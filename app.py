import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Meridian Forward | Team 10", page_icon="📊", layout="wide")

st.markdown("""
<style>
.block-container {padding-top: 2rem; padding-bottom: 3rem; max-width: 1150px;}
.hero {padding: 1.7rem 1.8rem; border-radius: 16px; background: linear-gradient(120deg,#102a43,#176b87); color: white;}
.hero h1 {font-size: 2.25rem; margin: 0 0 .35rem 0;}
.hero p {font-size: 1.05rem; margin: 0; opacity: .92;}
.kpi {background: white; padding: 1rem; border: 1px solid #d9e2ec; border-radius: 12px;}
.problem {background:#fff7ed; padding:1rem 1.2rem; border-left:5px solid #ea580c; border-radius:8px;}
.output {background:#eff6ff; padding:1rem 1.2rem; border-left:5px solid #2563eb; border-radius:8px;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>Meridian Forward</h1>
  <p>Problem & Output e-Portfolio | Team No. 10</p>
</div>
""", unsafe_allow_html=True)
st.write("")

st.markdown("### 1. Problem")
st.markdown("""
<div class="problem">
<strong>Core problem</strong><br>
The pilot needs sufficient vendor capacity to close the remaining workload gaps, but the estimated staffing cost must be evaluated against the available budget. The team must determine the resource requirement, calculate the cost implication, and decide whether the pilot plan is financially feasible.
</div>
""", unsafe_allow_html=True)
st.caption("This problem statement is a concise framing based on the calculation sheet; revise it if the official case brief states the problem differently.")

st.markdown("### 2. Inputs and assumptions")
with st.expander("View or adjust the case inputs", expanded=True):
    c1,c2,c3 = st.columns(3)
    with c1:
        weeks = st.number_input("Pilot duration (weeks)", min_value=1, max_value=52, value=4)
        hours_week = st.number_input("Paid hours per vendor / week", min_value=1, max_value=80, value=40)
        allowance_pct = st.slider("Non-productive time allowance (%)", 0, 50, 20, 5)
    with c2:
        proficiency_pct = st.slider("Proficiency factor (%)", 10, 100, 80, 5)
        data_gap = st.number_input("Data preparation gap (hours)", min_value=0, value=352, step=8)
        qa_gap = st.number_input("QA gap (hours)", min_value=0, value=96, step=8)
    with c3:
        legacy_gap = st.number_input("Legacy expert gap (hours)", min_value=0, value=96, step=8)
        cost_per_vendor = st.number_input("Estimated cost per vendor (₹)", min_value=0, value=106667, step=1000)
        budget_cap = st.number_input("Pilot budget cap (₹)", min_value=0, value=600000, step=10000)

paid_hours = weeks * hours_week
productive_hours = paid_hours * (1 - allowance_pct/100)
effective_hours = productive_hours * (proficiency_pct/100)
data_vendors = math.ceil(data_gap/effective_hours) if effective_hours else 0
qa_vendors = math.ceil(qa_gap/effective_hours) if effective_hours else 0
legacy_vendors = math.ceil(legacy_gap/effective_hours) if effective_hours else 0
total_vendors = data_vendors + qa_vendors + legacy_vendors
estimated_cost = total_vendors * cost_per_vendor
variance = budget_cap - estimated_cost

st.markdown("### 3. Output")
m1,m2,m3,m4 = st.columns(4)
m1.metric("Effective hours / vendor", f"{effective_hours:,.1f} h")
m2.metric("Vendors required", f"{total_vendors}")
m3.metric("Estimated cost", f"₹{estimated_cost:,.0f}")
m4.metric("Budget variance", f"₹{abs(variance):,.0f}", delta="Under budget" if variance > 0 else ("Over budget" if variance < 0 else "On budget"), delta_color="normal" if variance >= 0 else "inverse")

results = pd.DataFrame([
    {"Workstream":"Data preparation","Work gap (hours)":data_gap,"Vendors required":data_vendors},
    {"Workstream":"Quality assurance (QA)","Work gap (hours)":qa_gap,"Vendors required":qa_vendors},
    {"Workstream":"Legacy expertise","Work gap (hours)":legacy_gap,"Vendors required":legacy_vendors},
])
st.dataframe(results, use_container_width=True, hide_index=True)

st.markdown("### 4. Interpretation of the output")
if variance < 0:
    st.error(f"The current model estimates a cost of ₹{estimated_cost:,.0f}, which is ₹{abs(variance):,.0f} above the budget cap of ₹{budget_cap:,.0f}. The pilot is over budget under these assumptions.")
elif variance > 0:
    st.success(f"The current model estimates a cost of ₹{estimated_cost:,.0f}, leaving ₹{variance:,.0f} of the ₹{budget_cap:,.0f} budget unused.")
else:
    st.info(f"The current model estimates a cost of ₹{estimated_cost:,.0f}, exactly matching the budget cap.")

st.markdown("""
<div class="output">
<strong>Decision output</strong><br>
Use the staffing calculation to validate whether the required capacity can be secured within the budget. If the estimate exceeds the cap, the team should validate vendor rates and workload estimates, then consider phased staffing or reduced pilot scope before approval.
</div>
""", unsafe_allow_html=True)

st.markdown("### 5. Key result table")
summary = pd.DataFrame([
    ["Pilot duration", f"{weeks} weeks"],
    ["Paid hours per vendor", f"{paid_hours:,.0f} hours"],
    ["Effective hours per vendor", f"{effective_hours:,.1f} hours"],
    ["Total vendors required", str(total_vendors)],
    ["Estimated total cost", f"₹{estimated_cost:,.0f}"],
    ["Budget cap", f"₹{budget_cap:,.0f}"],
    ["Budget position", "Under budget" if variance > 0 else ("Over budget" if variance < 0 else "On budget")],
], columns=["Measure","Result"])
st.table(summary)

csv = results.to_csv(index=False).encode("utf-8")
st.download_button("Download output table (CSV)", data=csv, file_name="meridian_forward_team10_output.csv", mime="text/csv")

st.caption("Team No. 10 | Problem and output only. Verify all inputs against the official Meridian Forward case brief before submission.")
