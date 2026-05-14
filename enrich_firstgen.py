"""
Enrich data.json with first-generation student data from the College Scorecard
Most-Recent-Cohorts-Institution file.

Adds:
  - institutions[*].firstGen (float, share 0-1) where matched
  - top-level data["firstGen"] block with national aggregates:
      year, definition, source
      cosmetology: { value, n, enrollmentTotal }
      titleIVBenchmark: { value, n, enrollmentTotal }

Match strategy: normalize institution name + state and join.
Benchmark: all CURROPER=1 Scorecard rows EXCEPT those matched to a cosmetology-
flagged institution in data.json.
"""

import csv, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_JSON = os.path.join(HERE, "data", "data.json")
SCORECARD_CSV = os.environ.get(
    "SCORECARD_CSV",
    r"C:\Users\brady\AppData\Local\Temp\scorecard_inst\Most-Recent-Cohorts-Institution.csv",
)
SCORECARD_YEAR_LABEL = "2022-23 (Most-Recent-Cohorts, released April 2025)"

csv.field_size_limit(10_000_000)


def norm(s: str) -> str:
    if not s:
        return ""
    s = s.lower()
    s = s.replace("&", " and ")
    s = re.sub(r"[^a-z0-9]+", " ", s)
    s = re.sub(r"\b(the|inc|llc|incorporated|college|colleges|school|schools|of|at|a)\b", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def to_float(x):
    if x is None or x == "" or x == "NULL" or x == "PrivacySuppressed":
        return None
    try:
        return float(x)
    except (ValueError, TypeError):
        return None


def main():
    with open(DATA_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Loading Scorecard from: {SCORECARD_CSV}")
    sc_by_key = {}
    sc_rows = []
    with open(SCORECARD_CSV, "r", encoding="utf-8-sig") as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            sc_rows.append(row)
            key = (norm(row.get("INSTNM", "")), (row.get("STABBR") or "").upper())
            if key[0]:
                sc_by_key.setdefault(key, []).append(row)
    print(f"Scorecard rows loaded: {len(sc_rows)}")

    # Enrich each institution in data.json
    matched_cosm = 0
    matched_non = 0
    unmatched_cosm = []
    matched_unitids = set()  # UNITIDs that map to a cosmetology-flagged inst

    for inst in data["institutions"]:
        name = inst.get("institution", "")
        state = (inst.get("state") or "").upper()
        key = (norm(name), state)
        candidates = sc_by_key.get(key, [])
        sc = candidates[0] if candidates else None
        if sc:
            fg = to_float(sc.get("FIRST_GEN"))
            ugds = to_float(sc.get("UGDS"))
            inst["firstGen"] = fg
            inst["scorecardUgds"] = ugds
            if inst.get("cosmetologySchool"):
                matched_cosm += 1
                uid = sc.get("﻿UNITID") or sc.get("UNITID")
                if uid:
                    matched_unitids.add(uid)
            else:
                matched_non += 1
        else:
            inst["firstGen"] = None
            inst["scorecardUgds"] = None
            if inst.get("cosmetologySchool"):
                unmatched_cosm.append(f"{name} ({state})")

    total_cosm = sum(1 for i in data["institutions"] if i.get("cosmetologySchool"))
    print(f"Cosmetology institutions matched to Scorecard: {matched_cosm}/{total_cosm}")
    print(f"Non-cosmetology institutions matched: {matched_non}")
    print(f"Unmatched cosmetology institutions (first 10): {unmatched_cosm[:10]}")

    # --- Aggregate 1: cosmetology figure (enrollment-weighted FIRST_GEN) ---
    cosm_num, cosm_denom, cosm_n = 0.0, 0.0, 0
    for i in data["institutions"]:
        if not i.get("cosmetologySchool"):
            continue
        fg, w = i.get("firstGen"), i.get("scorecardUgds")
        if fg is None or w is None or w <= 0:
            continue
        cosm_num += fg * w
        cosm_denom += w
        cosm_n += 1
    cosm_value = (cosm_num / cosm_denom) if cosm_denom > 0 else None

    # --- Aggregate 2: Title IV benchmark from Scorecard ---
    # All CURROPER=1 institutions EXCEPT matched cosmetology UNITIDs.
    bench_num, bench_denom, bench_n = 0.0, 0.0, 0
    for row in sc_rows:
        if (row.get("CURROPER") or "0").strip() != "1":
            continue
        uid = row.get("﻿UNITID") or row.get("UNITID")
        if uid in matched_unitids:
            continue
        fg = to_float(row.get("FIRST_GEN"))
        ugds = to_float(row.get("UGDS"))
        if fg is None or ugds is None or ugds <= 0:
            continue
        bench_num += fg * ugds
        bench_denom += ugds
        bench_n += 1
    bench_value = (bench_num / bench_denom) if bench_denom > 0 else None

    data["firstGen"] = {
        "year": SCORECARD_YEAR_LABEL,
        "source": "U.S. Department of Education College Scorecard, Most-Recent-Cohorts-Institution file (released April 2025).",
        "definition": "Share of students whose parents' highest educational attainment is a high school diploma or less (Scorecard variable FIRST_GEN).",
        "method": "Enrollment-weighted mean across institutions, using Scorecard undergraduate enrollment (UGDS) as the weight. Institutions with suppressed or missing FIRST_GEN or zero/missing UGDS were excluded.",
        "cosmetology": {
            "value": round(cosm_value, 4) if cosm_value is not None else None,
            "n": cosm_n,
            "enrollmentTotal": int(round(cosm_denom)),
        },
        "titleIVBenchmark": {
            "value": round(bench_value, 4) if bench_value is not None else None,
            "n": bench_n,
            "enrollmentTotal": int(round(bench_denom)),
        },
    }

    print()
    print("Cosmetology first-gen share: {:.1%} (n={}, enrollment={:,})".format(
        cosm_value or 0, cosm_n, int(round(cosm_denom))))
    print("Title IV benchmark first-gen share: {:.1%} (n={}, enrollment={:,})".format(
        bench_value or 0, bench_n, int(round(bench_denom))))
    print("Delta (cosmetology - benchmark): {:+.1f} pp".format(
        ((cosm_value or 0) - (bench_value or 0)) * 100))

    with open(DATA_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"\nWrote {DATA_JSON}")


if __name__ == "__main__":
    main()
