import streamlit as st

st.set_page_config(page_title="Fix-Up Estimator", page_icon="🏠", layout="centered")

st.title("🏠 Remodel Cost Predictor")
st.caption("Driven by Portfolio Historical Data (25 Properties)")

# --- STEP 1: PROPERTY SPECS ---
st.subheader("1. Property Specifications")
col1, col2 = st.columns(2)

with col1:
    sqft = st.number_input("Finished Sq Footage", min_value=400, max_value=6000, value=1800, step=50)
    year_built = st.number_input("Year Built", min_value=1900, max_value=2026, value=1968, step=1)

with col2:
    prop_type = st.selectbox("Property Style", ["Ranch", "Townhouse", "Condo", "2-Story", "Tri-Level", "Bi-Level"])
    level = st.select_slider(
        "Renovation Level",
        options=["Level 1: Minor/Touch-Up", "Level 2: Medium/Cosmetics", "Level 3: Full Remodel"],
        value="Level 2: Medium/Cosmetics"
    )

# --- BASE PSF ENGINE ---
psf_rates = {
    "Level 1: Minor/Touch-Up": 16.00,
    "Level 2: Medium/Cosmetics": 38.06,
    "Level 3: Full Remodel": 78.03
}
base_psf = psf_rates[level]
base_cost = sqft * base_psf

# --- STEP 2: AGE RISK AUTO-DETECTION ---
is_pre_1970 = year_built < 1970
if is_pre_1970:
    st.warning("⚠️ **Pre-1970 Build Detected:** Higher baseline risk for cast iron sewer, knob-and-tube/panel updates, and abatement.")

# --- STEP 3: SCOPE TRIGGERS ---
st.subheader("2. Infrastructure & Major Add-Ons")
st.caption("Check items required outside standard cosmetic scope:")

col_a, col_b = st.columns(2)
with col_a:
    has_kitchen = st.checkbox("New Kitchen Cabinets & Slabs (~$8,500)", value=(level == "Level 3: Full Remodel"))
    has_sewer = st.checkbox("Main Sewer Line Replacement (~$11,400)", value=(is_pre_1970 and level == "Level 3: Full Remodel"))
    has_roof = st.checkbox("Complete Roof & Gutters (~$11,000)")

with col_b:
    has_rewire = st.checkbox("Full Rewire / Panel Upgrade (~$8,500)", value=(is_pre_1970 and level == "Level 3: Full Remodel"))
    has_concrete = st.checkbox("Driveway / Concrete Flatwork (~$7,500)")
    has_abatement = st.checkbox("Asbestos / Lead Abatement (~$3,500)", value=is_pre_1970)

# --- CALCULATION LOGIC ---
add_ons = 0
if has_kitchen and level != "Level 3: Full Remodel": add_ons += 8500
if has_sewer: add_ons += 11400
if has_roof: add_ons += 11000
if has_rewire: add_ons += 8500
if has_concrete: add_ons += 7500
if has_abatement: add_ons += 3500

total_estimate = base_cost + add_ons
low_range = total_estimate * 0.92
high_range = total_estimate * 1.08
effective_psf = total_estimate / sqft

# --- ESTIMATE DISPLAY ---
st.divider()
st.metric("Predicted Total Renovation Cost", f"${total_estimate:,.0f}", delta=f"${effective_psf:.2f}/sq ft")
st.write(f"**Target Budget Range:** ${low_range:,.0f} — ${high_range:,.0f}")

# --- SUB-TRADE BUDGET ALLOCATION ---
st.subheader("3. Expected Sub-Trade Budget Allocation")
st.caption("Based on portfolio historical expenditure weights (Medina reclassified to Construction):")

allocations = {
    "General Contract Labor (29.4%)": total_estimate * 0.294,
    "Raw Materials (23.4%)": total_estimate * 0.234,
    "Plumbing & Sewer (7.5%)": total_estimate * 0.075,
    "Roofing & Gutters (5.0%)": total_estimate * 0.050,
    "HVAC Systems (4.2%)": total_estimate * 0.042,
    "Flooring (3.8%)": total_estimate * 0.038,
    "Painting - Actual (3.3%)": total_estimate * 0.033,
    "Electrical (3.0%)": total_estimate * 0.030,
    "Countertops & Cabinets (4.8%)": total_estimate * 0.048,
    "Other / Contingency (12.2%)": total_estimate * 0.122,
}

for trade, amount in allocations.items():
    st.write(f"• **{trade}:** ${amount:,.0f}")