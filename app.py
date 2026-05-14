import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json, os

st.set_page_config(page_title="AACS Cosmetology Industry Data Explorer", layout="wide", page_icon=":scissors:")

# --- AACS Colors ---
NAVY = "#18223a"
BLUE = "#4a68b0"
GOLD = "#cfa158"
LIGHT = "#d9e1f3"
DARK_TEXT = "#363430"
COLORS = ["#4a68b0", "#cfa158", "#18223a", "#b0453a", "#7a5520", "#6b8cce", "#d9a44e", "#363430", "#8fa3d4", "#e8c882"]

# --- Custom CSS ---
st.markdown(f"""
<style>
    .block-container {{ padding-top: 1rem; }}
    [data-testid="stMetric"] {{
        background: white;
        border: 1px solid {LIGHT};
        border-radius: 8px;
        padding: 12px 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,.06);
    }}
    [data-testid="stMetric"] [data-testid="stMetricValue"] {{
        color: {GOLD};
        font-size: 1.8rem;
    }}
    .footnote {{
        font-size: 0.72rem;
        color: #5b5b5b;
        line-height: 1.6;
        border-top: 1px solid {LIGHT};
        padding-top: 12px;
        margin-top: 20px;
    }}
    div[data-testid="stTabs"] button[data-baseweb="tab"] {{
        font-size: 0.9rem;
    }}
    div[data-testid="stTabs"] button[aria-selected="true"] {{
        border-bottom-color: {GOLD} !important;
    }}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown(f"""
<div style="background:linear-gradient(135deg,{NAVY},#2a3a5c);color:white;padding:20px 32px;border-radius:8px;margin-bottom:16px;display:flex;align-items:center;gap:24px;">
<svg width="200" height="52" viewBox="0 0 400 104" xmlns="http://www.w3.org/2000/svg">
<text x="0" y="82" font-family="Georgia,serif" font-size="96" font-weight="400" fill="#6B8CCE" letter-spacing="-2">AACS</text>
<line x1="262" y1="12" x2="262" y2="92" stroke="{GOLD}" stroke-width="2"/>
<text x="274" y="32" font-family="Georgia,serif" font-size="20" font-weight="700" fill="{GOLD}" letter-spacing="2">AMERICAN</text>
<text x="274" y="52" font-family="Georgia,serif" font-size="20" font-weight="700" fill="{GOLD}" letter-spacing="2">ASSOCIATION</text>
<text x="274" y="72" font-family="Georgia,serif" font-size="20" font-weight="700" fill="{GOLD}" letter-spacing="2">OF CAREER</text>
<text x="274" y="92" font-family="Georgia,serif" font-size="20" font-weight="700" fill="{GOLD}" letter-spacing="2">SCHOOLS</text>
</svg>
<div>
<h2 style="margin:0;font-size:1.5rem;">Cosmetology Industry Data Explorer</h2>
<p style="margin:4px 0 0;opacity:0.85;font-size:0.85rem;">Barber, Beauty, and Wellness Schools: Setting the Record Straight</p>
</div>
</div>
""", unsafe_allow_html=True)

# --- Load Data ---
@st.cache_data
def load_data():
    path = os.path.join(os.path.dirname(__file__), "data", "data.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

D = load_data()

# --- Helper: Plotly layout ---
def base_layout(title="", yaxis_title="", y_tickprefix="", y_ticksuffix=""):
    return dict(
        template="plotly_white",
        title=dict(text=title, font=dict(size=14, color=NAVY)),
        font=dict(family="Segoe UI, sans-serif", color=DARK_TEXT),
        margin=dict(l=50, r=20, t=40, b=40),
        height=380,
        yaxis=dict(title=yaxis_title, tickprefix=y_tickprefix, ticksuffix=y_ticksuffix),
        legend=dict(orientation="h", y=-0.15)
    )

# --- TABS ---
tab_overview, tab_comp, tab_emp, tab_fin, tab_inst, tab_prog, tab_demo = st.tabs(
    ["Overview", "Completions", "Employment", "Finances", "Institutional Outcomes", "Program Outcomes", "Student Demographics"]
)

# ===========================
# OVERVIEW
# ===========================
with tab_overview:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Cosmetology Schools Nationwide*", "1,326")
    c2.metric("Estimated Market Size**", "$3.3B")
    c3.metric("Completions in 2024 (10-Yr High)", "160K")
    c4.metric("Est. Taxes Paid (FY2023)", "$205M+")

    # Market size chart
    mkt_years = list(range(2014, 2031))
    mkt_est = [2.49, 2.55, 2.61, 2.68, 2.74, 2.80, None, None, None, None, None, None, None, None, None, None, None]
    mkt_actual = [None, None, None, None, None, 2.80, 2.79, 2.72, 3.18, 3.30, None, None, None, None, None, None, None]
    mkt_proj = [None, None, None, None, None, None, None, None, None, 3.30, 3.46, 3.63, 3.80, 3.98, 4.17, 4.37, 4.58]

    fig_mkt = go.Figure()
    fig_mkt.add_trace(go.Scatter(x=mkt_years, y=mkt_est, mode="lines+markers+text", name="Estimated (2014-2018)",
        line=dict(color=GOLD, dash="dash", width=2), marker=dict(size=6), text=["$"+str(v)+"B" if v else "" for v in mkt_est], textposition="top center", textfont=dict(size=9)))
    fig_mkt.add_trace(go.Scatter(x=mkt_years, y=mkt_actual, mode="lines+markers+text", name="Actual (IPEDS, 2019-2023)",
        line=dict(color=GOLD, width=3), marker=dict(size=8), fill="tozeroy", fillcolor="rgba(207,161,88,0.12)",
        text=["$"+str(v)+"B" if v else "" for v in mkt_actual], textposition="top center", textfont=dict(size=9)))
    fig_mkt.add_trace(go.Scatter(x=mkt_years, y=mkt_proj, mode="lines+markers+text", name="Projected (4.8% Growth)",
        line=dict(color=GOLD, dash="dash", width=3), marker=dict(size=6),
        text=["$"+str(v)+"B" if v else "" for v in mkt_proj], textposition="top center", textfont=dict(size=9)))
    fig_mkt.update_layout(**base_layout("Cosmetology School Market Size: Updated Analysis", "Market Size ($B)", "$", "B"))
    fig_mkt.update_yaxes(rangemode="tozero")
    st.plotly_chart(fig_mkt, use_container_width=True)

    # Completions & Employment charts
    col1, col2 = st.columns(2)
    with col1:
        total_row = next((c for c in D["completionsNational"] if c["awardLevel"] == "Total"), None)
        if total_row:
            vals = total_row["values"]
        else:
            vals = [sum(c["values"][i] for c in D["completionsNational"]) for i in range(len(D["completionsYears"]))]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=D["completionsYears"], y=vals, mode="lines+markers", fill="tozeroy",
            line=dict(color=BLUE, width=2), fillcolor=f"rgba(74,104,176,0.12)"))
        fig.update_layout(**base_layout("National Completions Trend (2015-2024)"))
        fig.update_yaxes(rangemode="tozero", tickformat=",")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        emp_total = next((e for e in D["employmentNational"] if e["occupation"] == "Total"), None)
        if emp_total:
            all_years = D["empActualYears"] + D["empProjectedYears"]
            all_vals = emp_total["actual"] + emp_total["projected"]
            n_actual = len(D["empActualYears"])
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=all_years[:n_actual], y=all_vals[:n_actual], mode="lines+markers",
                name="Actual", line=dict(color="#38a169", width=2), fill="tozeroy", fillcolor="rgba(56,161,105,0.12)"))
            fig.add_trace(go.Scatter(x=all_years[n_actual-1:], y=all_vals[n_actual-1:], mode="lines+markers",
                name="Projected", line=dict(color="#38a169", width=2, dash="dash")))
            fig.update_layout(**base_layout("National Employment Trend (2012-2032)"))
            fig.update_yaxes(rangemode="tozero", tickformat=",")
            st.plotly_chart(fig, use_container_width=True)

    with st.expander("Executive Summary", expanded=False):
        st.write("This dashboard synthesizes findings from IPEDS and BLS datasets covering cosmetology and related personal services programs across all 50 states and the District of Columbia.")
        st.write("The data reveal an industry that experienced a COVID-era contraction followed by a strong recovery, with total program completions climbing from approximately 115,600 in 2019 to over 160,000 in 2024. Employment across all cosmetology occupations has similarly rebounded from a pandemic trough of roughly 526,000 workers in 2020 to over 631,000 by 2024, with further growth projected through 2032.")
        st.write("Financially, for-profit cosmetology schools contribute substantial tax revenue at the federal, state, and local levels, generating a combined estimated tax burden of $155-$210 million annually across the FY2019-FY2023 period while receiving relatively modest public appropriations in return.")

    st.markdown("""<div class="footnote">
<p><b>Sources:</b> IPEDS Completions Component (2015-2024); BLS Occupational Employment &amp; Wage Statistics and Employment Projections (2012-2032); IPEDS Finance Component, F3 Surveys (FY2019-FY2023).</p>
<p>*The 1,326 cosmetology schools figure is sourced from IBISWorld industry data. IPEDS institutional data identifies 1,026 cosmetology-designated schools; the difference reflects institutions not captured in IPEDS reporting.</p>
<p>**Previous industry estimates of $2.2B in market revenue were sourced from IBISWorld. Our updated analysis using IPEDS Finance data across all reporting for-profit cosmetology institutions yields an estimated market size of $3.3B, reflecting broader institutional coverage and more recent fiscal year data. Market size values for 2014-2018 in the chart are extrapolated backward from the 2019 IPEDS baseline using IBISWorld's historical growth trend. Values for 2024-2030 are projected forward at 4.8% annual growth.</p>
<p>Tax estimates are modeled using published federal and state tax rates and represent approximations, not audited tax returns. Prepared for the American Association of Career Schools (AACS) by Validated Insights.</p>
</div>""", unsafe_allow_html=True)

# ===========================
# COMPLETIONS
# ===========================
with tab_comp:
    view = st.selectbox("View", ["National by Program", "By State"], key="comp_view")
    years = D["completionsYears"]

    if view == "National by Program":
        top = [c for c in D["completionsNational"] if c["awardLevel"] != "Total" and c["total"] > 20000][:8]
        col1, col2 = st.columns(2)
        with col1:
            fig = go.Figure()
            for i, c in enumerate(top):
                fig.add_trace(go.Scatter(x=years, y=c["values"], mode="lines", name=c["cipTitle"][:30],
                    line=dict(color=COLORS[i % len(COLORS)], width=2)))
            fig.update_layout(**base_layout("Completions Over Time by Program"))
            fig.update_yaxes(tickformat=",")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            by_prog = sorted([c for c in D["completionsNational"] if c["awardLevel"] != "Total" and c["values"][9] > 500],
                key=lambda x: x["values"][9], reverse=True)[:10]
            fig = go.Figure(go.Bar(y=[c["cipTitle"][:25] for c in by_prog], x=[c["values"][9] for c in by_prog],
                orientation="h", marker_color=COLORS[:len(by_prog)]))
            fig.update_layout(**base_layout("Completions by Category (2024)"))
            fig.update_yaxes(autorange="reversed")
            st.plotly_chart(fig, use_container_width=True)

        rows = []
        for c in D["completionsNational"]:
            row = {"Award Level": c["awardLevel"], "Program": c["cipTitle"]}
            for i, y in enumerate(years):
                row[str(y)] = c["values"][i]
            row["10-Yr Total"] = c["total"]
            row["15-24 Change (%)"] = c["change"]
            rows.append(row)
        st.dataframe(pd.DataFrame(rows), use_container_width=True, height=500)
    else:
        st_data = D["stateCompletions"]
        state = st.selectbox("State", ["All States"] + sorted(st_data.keys()), key="comp_state")
        if state == "All States":
            col1, col2 = st.columns(2)
            with col1:
                sorted_st = sorted(st_data.items(), key=lambda x: x[1][9], reverse=True)[:20]
                fig = go.Figure(go.Bar(x=[s[0] for s in sorted_st], y=[s[1][9] for s in sorted_st], marker_color=BLUE))
                fig.update_layout(**base_layout("Top States by Completions (2024)"))
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                growth = [(s, ((v[9]-v[0])/v[0]*100) if v[0] > 0 else None) for s, v in st_data.items()]
                growth = sorted([(s, g) for s, g in growth if g is not None], key=lambda x: x[1], reverse=True)[:15]
                fig = go.Figure(go.Bar(x=[g[0] for g in growth], y=[round(g[1]) for g in growth],
                    marker_color=[("#38a169" if g[1] >= 0 else "#e53e3e") for g in growth]))
                fig.update_layout(**base_layout("10-Year Growth by State (%)"))
                st.plotly_chart(fig, use_container_width=True)
        else:
            vals = st_data.get(state, [])
            fig = go.Figure(go.Scatter(x=years, y=vals, mode="lines+markers", fill="tozeroy",
                line=dict(color=BLUE, width=2), fillcolor=f"rgba(74,104,176,0.12)"))
            fig.update_layout(**base_layout(f"{state} Completions Over Time"))
            st.plotly_chart(fig, use_container_width=True)

        rows = []
        for s, v in sorted(st_data.items(), key=lambda x: x[1][9], reverse=True):
            row = {"State": s}
            for i, y in enumerate(years):
                row[str(y)] = v[i]
            row["Total"] = sum(v)
            row["15-24 Change (%)"] = round((v[9]-v[0])/v[0]*100, 1) if v[0] > 0 else None
            rows.append(row)
        st.dataframe(pd.DataFrame(rows), use_container_width=True, height=500)

    st.markdown("""<div class="footnote">
<p><b>Source:</b> IPEDS Completions Component (2015-2024), all 50 states and the District of Columbia.</p>
<p><b>CIP codes included:</b> CIP 12.04xx (Cosmetology and Related Personal Grooming Services) — including 12.0401 Cosmetology/Cosmetologist General, 12.0402 Barbering/Barber, 12.0404 Aesthetician/Esthetician, 12.0406 Make-Up Artist, 12.0407 Hair Styling, 12.0408 Facial Treatment Specialist, 12.0409 Nail Technician, 12.0410 Master Aesthetician, 12.0411 Permanent Cosmetics, 12.0412 Salon Management, 12.0413 Cosmetology Instructor, 12.0414 Electrolysis, 12.0499 Other. Also includes CIP 51.35xx (Somatic Bodywork and Related Therapeutic Services) — 51.3501 Massage Therapy, 51.3502 Asian Bodywork Therapy, 51.3503 Somatic Bodywork, 51.3599 Other.</p>
<p>Completions represent credentials awarded at all award levels (certificates &lt;1 year, 1-2 year certificates, 2-4 year certificates, and associate degrees). "15-24 Change (%)" compares 2024 to 2015 values.</p>
</div>""", unsafe_allow_html=True)

# ===========================
# EMPLOYMENT
# ===========================
with tab_emp:
    view = st.selectbox("View", ["National by Occupation", "By State (Total)"], key="emp_view")
    emp_years = D["empActualYears"]
    proj_years = D["empProjectedYears"]

    if view == "National by Occupation":
        occs = [e for e in D["employmentNational"] if e["occupation"] != "Total"]
        col1, col2 = st.columns(2)
        with col1:
            all_y = emp_years + proj_years
            n_act = len(emp_years)
            fig = go.Figure()
            for i, e in enumerate(occs):
                all_v = e["actual"] + e["projected"]
                fig.add_trace(go.Scatter(x=all_y[:n_act], y=all_v[:n_act], mode="lines", name=e["occupation"][:30],
                    line=dict(color=COLORS[i % len(COLORS)], width=2), showlegend=True))
                fig.add_trace(go.Scatter(x=all_y[n_act-1:], y=all_v[n_act-1:], mode="lines",
                    line=dict(color=COLORS[i % len(COLORS)], width=2, dash="dash"), showlegend=False))
            fig.update_layout(**base_layout("Employment Trend with Projections"))
            fig.update_yaxes(tickformat=",")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            bar_data = sorted([e for e in occs if e["actual"][12]], key=lambda x: x["actual"][12] or 0, reverse=True)
            fig = go.Figure(go.Bar(y=[e["occupation"][:25] for e in bar_data], x=[e["actual"][12] for e in bar_data],
                orientation="h", marker_color=COLORS[:len(bar_data)]))
            fig.update_layout(**base_layout("Employment by Occupation (2024)"))
            fig.update_yaxes(autorange="reversed")
            st.plotly_chart(fig, use_container_width=True)

        rows = []
        for e in D["employmentNational"]:
            is_total = e["occupation"] == "Total"
            rows.append({
                "Occupation": e["occupation"],
                "2012": e["actual"][0], "2022": e["actual"][10],
                "2024": e["actual"][12], "2032p": e["projected"][7],
                "12-22 Change (%)": e["chg1222"], "22-32 Change (%)": e["chg2232"]
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, height=400)
    else:
        st_emp = D["stateEmployment"]
        col1, col2 = st.columns(2)
        with col1:
            sorted_st = sorted([(s, v) for s, v in st_emp.items() if v["actual"][10]], key=lambda x: x[1]["actual"][10] or 0, reverse=True)[:25]
            fig = go.Figure(go.Bar(x=[s[0] for s in sorted_st], y=[s[1]["actual"][10] for s in sorted_st], marker_color=BLUE))
            fig.update_layout(**base_layout("Top States by Employment (2022)"))
            fig.update_yaxes(tickformat=",")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            growth = [(s, (v["actual"][10]-v["actual"][0])/v["actual"][0]*100) for s, v in st_emp.items() if v["actual"][0] and v["actual"][10]]
            growth = sorted(growth, key=lambda x: x[1], reverse=True)[:15]
            fig = go.Figure(go.Bar(x=[g[0] for g in growth], y=[round(g[1]) for g in growth],
                marker_color=[("#38a169" if g[1] >= 0 else "#e53e3e") for g in growth]))
            fig.update_layout(**base_layout("2012-2022 Employment Growth by State (%)"))
            st.plotly_chart(fig, use_container_width=True)

        rows = []
        for s, v in sorted(st_emp.items(), key=lambda x: x[1]["actual"][10] or 0, reverse=True):
            chg = round((v["actual"][10]-v["actual"][0])/v["actual"][0]*100, 1) if v["actual"][0] and v["actual"][10] else None
            rows.append({
                "State": s, "2012": v["actual"][0], "2022": v["actual"][10],
                "2024": v["actual"][12], "2032p": v["proj2032"],
                "12-22 Change (%)": chg, "22-32 Change (%)": v["chg2232"]
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, height=500)

    st.markdown("""<div class="footnote">
<p><b>Source:</b> BLS Occupational Employment &amp; Wage Statistics (OEWS) for 2012-2024 actual data; BLS Employment Projections for 2025-2032 projected values (denoted with "p").</p>
<p><b>Occupations included:</b> Hairdressers, Hairstylists, and Cosmetologists (SOC 39-5012); Barbers (39-5011); Manicurists and Pedicurists (39-5092); Skincare Specialists (39-5094); Shampooers (39-5093); Massage Therapists (31-9011); Makeup Artists, Theatrical and Performance (39-5091). Dashed lines on charts indicate projected values. State-level projections are interpolated from BLS 10-year projection models.</p>
</div>""", unsafe_allow_html=True)

# ===========================
# FINANCES
# ===========================
with tab_fin:
    view = st.selectbox("View", ["National Aggregate", "By State"], key="fin_view")
    fn = D["financeNational"]

    if view == "National Aggregate":
        col1, col2 = st.columns(2)
        with col1:
            fy_labels = [f"FY{f['year']}" for f in fn]
            fig = go.Figure()
            fig.add_trace(go.Bar(x=fy_labels, y=[f["revenue"] for f in fn], name="Revenue ($B)", marker_color=BLUE, text=[f"${f['revenue']}" for f in fn], textposition="outside"))
            fig.add_trace(go.Bar(x=fy_labels, y=[f["expenses"] for f in fn], name="Expenses ($B)", marker_color="#b0453a", text=[f"${f['expenses']}" for f in fn], textposition="outside"))
            fig.add_trace(go.Bar(x=fy_labels, y=[f["netIncome"] for f in fn], name="Net Income ($B)", marker_color="#38a169", text=[f"${f['netIncome']}" for f in fn], textposition="outside"))
            fig.update_layout(**base_layout("Revenue & Expenses ($B)"), barmode="group")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = go.Figure()
            fig.add_trace(go.Bar(x=fy_labels, y=[f["fedTax"] for f in fn], name="Federal Tax ($M)", marker_color=BLUE, text=[f"${f['fedTax']}" for f in fn], textposition="outside"))
            fig.add_trace(go.Bar(x=fy_labels, y=[f["stateTax"] for f in fn], name="State/Local Tax ($M)", marker_color="#7a5520", text=[f"${f['stateTax']}" for f in fn], textposition="outside"))
            fig.update_layout(**base_layout("Tax Contributions ($M)"))
            st.plotly_chart(fig, use_container_width=True)

        rows = []
        for f in fn:
            rows.append({
                "Year": f"FY{f['year']}", "Revenue ($B)": f["revenue"], "Expenses ($B)": f["expenses"],
                "Net Income ($B)": f["netIncome"], "Federal Tax ($M)": f["fedTax"],
                "State/Local Tax ($M)": f["stateTax"], "Total Tax ($M)": round(f["fedTax"] + f["stateTax"], 1)
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
    else:
        st_fin = D["financeByState"]
        state = st.selectbox("State", ["All States"] + sorted(st_fin.keys()), key="fin_state")
        if state != "All States" and state in st_fin:
            sd = st_fin[state]
            col1, col2 = st.columns(2)
            with col1:
                fy = [f"FY{f['year']}" for f in sd]
                fig = go.Figure()
                fig.add_trace(go.Bar(x=fy, y=[f["revenue"] for f in sd], name="Revenue ($B)", marker_color=BLUE))
                fig.add_trace(go.Bar(x=fy, y=[f["expenses"] for f in sd], name="Expenses ($B)", marker_color="#b0453a"))
                fig.update_layout(**base_layout(f"{state} Revenue & Expenses ($B)"), barmode="group")
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                fig = go.Figure()
                fig.add_trace(go.Bar(x=fy, y=[f.get("fedTax", 0) for f in sd], name="Federal Tax ($M)", marker_color=BLUE))
                fig.add_trace(go.Bar(x=fy, y=[f.get("stateTax", 0) for f in sd], name="State/Local Tax ($M)", marker_color="#7a5520"))
                fig.update_layout(**base_layout(f"{state} Tax Contributions ($M)"))
                st.plotly_chart(fig, use_container_width=True)
        else:
            col1, col2 = st.columns(2)
            with col1:
                latest = {s: arr[-1]["revenue"] for s, arr in st_fin.items()}
                sorted_s = sorted(latest.items(), key=lambda x: x[1], reverse=True)[:20]
                fig = go.Figure(go.Bar(x=[s[0] for s in sorted_s], y=[s[1] for s in sorted_s], marker_color=BLUE))
                fig.update_layout(**base_layout("Revenue by State ($B)"))
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                latest_tax = {s: (arr[-1].get("fedTax", 0) or 0) + (arr[-1].get("stateTax", 0) or 0) for s, arr in st_fin.items()}
                sorted_t = sorted([(s, v) for s, v in latest_tax.items() if v > 0], key=lambda x: x[1], reverse=True)[:20]
                fig = go.Figure(go.Bar(x=[s[0] for s in sorted_t], y=[s[1] for s in sorted_t], marker_color=GOLD))
                fig.update_layout(**base_layout("Total Tax by State ($M)"))
                st.plotly_chart(fig, use_container_width=True)

        rows = []
        for s, arr in sorted(st_fin.items(), key=lambda x: x[1][-1]["revenue"], reverse=True):
            last = arr[-1]
            rows.append({"State": s, "Latest Revenue ($M)": round(last["revenue"]*1000, 1), "Latest Expenses ($M)": round(last["expenses"]*1000, 1)})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, height=500)

    st.markdown("""<div class="footnote">
<p><b>Source:</b> IPEDS Finance Component, F3 Surveys (FY2019-FY2023). Covers cosmetology-designated for-profit institutions only.</p>
<p>Tax estimates are modeled using standard corporate income tax rates, payroll tax rates (Social Security, Medicare, FUTA, SUTA), property tax proxies, and city-level tax schedules where applicable. These are estimates, not audited tax returns.</p>
</div>""", unsafe_allow_html=True)

# ===========================
# INSTITUTIONAL OUTCOMES
# ===========================
with tab_inst:
    col_f1, col_f2, col_f3 = st.columns(3)
    search = col_f1.text_input("Search institution", key="inst_search")
    states = sorted(set(i["state"] for i in D["institutions"] if i["state"]))
    state = col_f2.selectbox("State", ["All States"] + states, key="inst_state")
    cosm_filter = col_f3.selectbox("Filter", ["All Cosmetology Schools", "AACS Members Only"], key="inst_cosm")

    filtered = [i for i in D["institutions"] if i["cosmetologySchool"]]
    if cosm_filter == "AACS Members Only":
        filtered = [i for i in filtered if i["aacsMember"]]
    if state != "All States":
        filtered = [i for i in filtered if i["state"] == state]
    if search:
        filtered = [i for i in filtered if search.lower() in i["institution"].lower()]

    col1, col2 = st.columns(2)
    with col1:
        rates = [i["completionRate"] for i in filtered if i["completionRate"] is not None]
        fig = go.Figure(go.Histogram(x=rates, nbinsx=10, marker_color=BLUE))
        fig.update_layout(**base_layout("Completion Rate Distribution", "Count"), xaxis=dict(title="Completion Rate (%)"))
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        earns = [i["medianEarnings"] for i in filtered if i["medianEarnings"] is not None]
        fig = go.Figure(go.Histogram(x=earns, nbinsx=10, marker_color="#38a169"))
        fig.update_layout(**base_layout("Median Earnings (10yr) Distribution", "Count"), xaxis=dict(title="Median Earnings ($)", tickprefix="$", tickformat=","))
        st.plotly_chart(fig, use_container_width=True)

    rows = []
    for i in filtered[:200]:
        rows.append({
            "Institution": i["institution"], "State": i["state"], "Type": i["ownership"],
            "Enrollment": i["enrollment"],
            "Completion Rate (%)": i["completionRate"],
            "Median Earnings (10yr)": i["medianEarnings"],
            "Median Debt": i["medianDebt"],
            "AACS": "Yes" if i["aacsMember"] else ""
        })
    st.write(f"**Institutional Outcomes ({len(filtered)} shown)**")
    st.dataframe(pd.DataFrame(rows), use_container_width=True, height=500)

    st.markdown("""<div class="footnote">
<p><b>Source:</b> U.S. Department of Education College Scorecard; IPEDS Institutional Characteristics and Student Financial Aid surveys. Only cosmetology-designated schools are shown.</p>
<p>Institution-level outcomes are reported at the school level, not by CIP code. Earnings and debt figures reflect all programs at the institution and are not limited to CIP 12.04. Completion rates reflect the IPEDS 150%-time graduation rate for programs under 4 years. Median Earnings (10yr) represent median earnings of federal financial aid recipients 10 years after enrollment. "AACS" denotes membership in the American Association of Career Schools.</p>
</div>""", unsafe_allow_html=True)

# ===========================
# PROGRAM OUTCOMES
# ===========================
with tab_prog:
    col_f1, col_f2, col_f3 = st.columns(3)
    search = col_f1.text_input("Search institution or program", key="prog_search")
    prog_states = sorted(set(p["state"] for p in D["programs"] if p["state"]))
    state = col_f2.selectbox("State", ["All States"] + prog_states, key="prog_state")
    cosm_filter = col_f3.selectbox("Filter", ["All Programs", "Cosmetology Schools Only", "AACS Members Only"], key="prog_cosm")

    filtered = D["programs"]
    if cosm_filter == "Cosmetology Schools Only":
        filtered = [p for p in filtered if p["cosmetologySchool"]]
    elif cosm_filter == "AACS Members Only":
        filtered = [p for p in filtered if p["aacsMember"]]
    if state != "All States":
        filtered = [p for p in filtered if p["state"] == state]
    if search:
        filtered = [p for p in filtered if search.lower() in p["institution"].lower() or search.lower() in p["programTitle"].lower()]

    # Earnings chart
    all_progs = [p for p in D["programs"] if p["state"] == state] if state != "All States" else D["programs"]
    cosm_progs = [p for p in all_progs if p["cosmetologySchool"]]
    non_cosm_progs = [p for p in all_progs if not p["cosmetologySchool"]]

    def weighted_avg(progs, field):
        s_we, s_w = 0, 0
        for p in progs:
            e, w = p.get(field), p.get("awards2") or p.get("awards1") or 0
            if e and w > 0:
                s_we += e * w; s_w += w
        return round(s_we / s_w) if s_w > 0 else None

    earn_fields = ["earn1yr", "earn2yr", "earn3yr", "earn4yr"]
    earn_labels = ["1 Year", "2 Years", "3 Years", "4 Years"]
    cosm_earn = [weighted_avg(cosm_progs, f) for f in earn_fields]
    non_cosm_earn = [weighted_avg(non_cosm_progs, f) for f in earn_fields]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=earn_labels, y=cosm_earn, mode="lines+markers+text", name="Cosmetology Schools",
        line=dict(color=BLUE, width=3), marker=dict(size=8),
        text=[f"${v//1000}K" if v else "" for v in cosm_earn], textposition="top center"))
    fig.add_trace(go.Scatter(x=earn_labels, y=non_cosm_earn, mode="lines+markers+text", name="Other Institutions",
        line=dict(color="#b0453a", width=3), marker=dict(size=8),
        text=[f"${v//1000}K" if v else "" for v in non_cosm_earn], textposition="top center"))
    fig.update_layout(**base_layout("Weighted Avg. Median Earnings: Cosmetology Schools vs. Other Institutions"))
    fig.update_yaxes(rangemode="tozero", tickprefix="$", tickformat=",")
    st.plotly_chart(fig, use_container_width=True)

    rows = []
    for p in filtered[:200]:
        rows.append({
            "Institution": p["institution"], "State": p["state"], "Program": p["programTitle"],
            "Level": p["credLevel"], "Awards Yr1": p["awards1"], "Awards Yr2": p["awards2"],
            "1yr Earnings": p["earn1yr"], "2yr Earnings": p["earn2yr"],
            "3yr Earnings": p["earn3yr"], "4yr Earnings": p["earn4yr"]
        })
    st.write(f"**Program Outcomes ({len(filtered)} shown)**")
    st.dataframe(pd.DataFrame(rows), use_container_width=True, height=500)

    st.markdown("""<div class="footnote">
<p><b>Source:</b> U.S. Department of Education College Scorecard, program-level data.</p>
<p><b>CIP codes included:</b> CIP 12.04 (Cosmetology and Related Personal Grooming Services) only. Note: The College Scorecard program-level outcomes data uses the 2-digit CIP prefix 12.04, which covers cosmetology, barbering, esthetics, nail technology, and related grooming programs. It does <b>not</b> include massage therapy or somatic bodywork programs (CIP 51.35xx), as those fall under a separate classification.</p>
<p>Earnings represent median earnings of Title IV financial aid recipients at 1, 2, 3, and 4 years after completion. Weighted averages in the chart use award counts as weights. "Cosmetology Schools" are institutions flagged as cosmetology-designated in IPEDS; "Other Institutions" are primarily community colleges and vocational schools offering cosmetology programs.</p>
</div>""", unsafe_allow_html=True)

# ===========================
# STUDENT DEMOGRAPHICS
# ===========================
with tab_demo:
    fg = D.get("firstGen", {})
    cosm = fg.get("cosmetology", {}) or {}
    bench = fg.get("titleIVBenchmark", {}) or {}
    cosm_val = cosm.get("value")
    bench_val = bench.get("value")

    st.markdown(f"<h3 style='color:{NAVY};margin:8px 0 4px;'>First-Generation Students</h3>", unsafe_allow_html=True)
    st.markdown(
        f"<p style='color:#5b5b5b;margin:0 0 16px;font-size:0.9rem;'>"
        f"Share of students at cosmetology schools who are the first in their family to attend college, "
        f"compared to all other Title IV institutions nationally.</p>",
        unsafe_allow_html=True,
    )

    if cosm_val is None or bench_val is None:
        st.warning("First-generation data not available in data.json. Run enrich_firstgen.py to populate.")
    else:
        delta_pp = (cosm_val - bench_val) * 100
        m1, m2, m3 = st.columns(3)
        m1.metric("Cosmetology Schools", f"{cosm_val*100:.1f}%")
        m2.metric("All Other Title IV Institutions", f"{bench_val*100:.1f}%")
        m3.metric("Difference", f"{delta_pp:+.1f} pp")

        fig = go.Figure(go.Bar(
            y=["Cosmetology Schools", "All Other Title IV Institutions"],
            x=[cosm_val * 100, bench_val * 100],
            orientation="h",
            marker_color=[GOLD, BLUE],
            text=[f"{cosm_val*100:.1f}%", f"{bench_val*100:.1f}%"],
            textposition="outside",
        ))
        fig.update_layout(**base_layout("% First-Generation Students (Enrollment-Weighted)"))
        fig.update_xaxes(ticksuffix="%", range=[0, max(cosm_val, bench_val) * 100 * 1.2])
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)

        summary = (
            f"Cosmetology schools enroll first-generation students at "
            f"<b>{cosm_val*100:.1f}%</b> &mdash; <b>{delta_pp:+.1f} percentage points</b> "
            f"{'above' if delta_pp >= 0 else 'below'} the national average of "
            f"<b>{bench_val*100:.1f}%</b> across all other Title IV institutions."
        )
        st.markdown(
            f"<div style='background:{LIGHT};padding:14px 18px;border-radius:8px;"
            f"border-left:4px solid {GOLD};margin-top:12px;font-size:0.95rem;'>{summary}</div>",
            unsafe_allow_html=True,
        )

    st.markdown(f"""<div class="footnote">
<p><b>Source:</b> {fg.get("source", "U.S. Department of Education College Scorecard.")} Data year: {fg.get("year", "most-recent cohort")}.</p>
<p><b>First-generation definition:</b> {fg.get("definition", "Share of students whose parents' highest educational attainment is a high school diploma or less.")}</p>
<p><b>Methodology:</b> {fg.get("method", "Enrollment-weighted mean across institutions.")} Cosmetology figure based on N={cosm.get("n", 0):,} institutions (total undergraduate enrollment {cosm.get("enrollmentTotal", 0):,}). Title IV benchmark based on N={bench.get("n", 0):,} institutions (total undergraduate enrollment {bench.get("enrollmentTotal", 0):,}). The benchmark excludes the cosmetology-designated institutions in the cosmetology figure.</p>
</div>""", unsafe_allow_html=True)
