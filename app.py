
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="A23 | Smart Home Agent",
    page_icon="⚡",
    layout="wide"
)

# ---------- SESSION DATA ----------
if "appliances" not in st.session_state:
    st.session_state.appliances = [
        {"name": "Air Conditioner", "watts": 1500, "hours": 6, "quantity": 1},
        {"name": "Refrigerator", "watts": 200, "hours": 12, "quantity": 1},
        {"name": "Ceiling Fan", "watts": 75, "hours": 10, "quantity": 3},
        {"name": "LED Lights", "watts": 12, "hours": 6, "quantity": 5}
    ]

# ---------- SIDEBAR ----------
st.sidebar.title("⚡ A23 SMART HOME")
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Appliances", "Energy Advisor", "Analytics", "Settings"]
)

st.sidebar.divider()
tariff = st.sidebar.number_input(
    "Electricity price (₹ / unit)",
    min_value=0.0,
    value=8.0,
    step=0.5
)

# ---------- CALCULATIONS ----------
df = pd.DataFrame(st.session_state.appliances)

if not df.empty:
    df["Daily kWh"] = (
        df["watts"] * df["hours"] * df["quantity"] / 1000
    )
    df["Monthly kWh"] = df["Daily kWh"] * 30
    df["Monthly Cost"] = df["Monthly kWh"] * tariff
    daily_units = df["Daily kWh"].sum()
else:
    daily_units = 0

monthly_units = daily_units * 30
monthly_bill = monthly_units * tariff

# ---------- HEADER ----------
st.title("⚡ A23 Smart Home Agent")
st.caption("Intelligent Home Energy Monitoring & Optimization")
st.divider()

# ---------- DASHBOARD ----------
if page == "Dashboard":

    st.subheader("Energy Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Daily Consumption", f"{daily_units:.2f} kWh")
    c2.metric("Monthly Consumption", f"{monthly_units:.2f} kWh")
    c3.metric("Estimated Bill", f"₹{monthly_bill:,.2f}")
    c4.metric("Appliances", len(df))

    st.subheader("Appliance Energy Consumption")

    if not df.empty:
        chart = px.bar(
            df,
            x="name",
            y="Daily kWh",
            color="Daily kWh",
            title="Daily Electricity Usage",
            labels={"name": "Appliance"}
        )
        st.plotly_chart(chart, use_container_width=True)
        st.dataframe(
            df[["name", "watts", "hours", "quantity",
                "Daily kWh", "Monthly Cost"]],
            use_container_width=True
        )
    else:
        st.info("Add appliances to see your dashboard.")

# ---------- APPLIANCES ----------
elif page == "Appliances":

    st.subheader("Manage Your Appliances")

    with st.form("appliance_form"):
        name = st.text_input("Appliance name")
        watts = st.number_input("Power rating (Watts)", min_value=1, value=100)
        hours = st.number_input("Daily usage (Hours)", min_value=0.0, max_value=24.0, value=5.0)
        quantity = st.number_input("Number of appliances", min_value=1, value=1)

        submitted = st.form_submit_button("Add Appliance")

        if submitted:
            if name.strip():
                st.session_state.appliances.append({
                    "name": name.strip(),
                    "watts": watts,
                    "hours": hours,
                    "quantity": quantity
                })
                st.success(f"{name} added successfully!")
                st.rerun()
            else:
                st.error("Please enter an appliance name.")

    st.divider()
    st.subheader("Your Appliances")

    if not df.empty:
        for i, appliance in enumerate(st.session_state.appliances):
            col1, col2 = st.columns([4, 1])
            col1.write(
                f"**{appliance['name']}** — "
                f"{appliance['watts']} W, "
                f"{appliance['hours']} hours/day"
            )
            if col2.button("Delete", key=f"delete_{i}"):
                st.session_state.appliances.pop(i)
                st.rerun()
    else:
        st.info("No appliances added yet.")

# ---------- ENERGY ADVISOR ----------
elif page == "Energy Advisor":

    st.subheader("🤖 Smart Energy Advisor")

    st.write("Recommendations based on your appliance usage data.")

    if not df.empty:
        for _, appliance in df.iterrows():
            if appliance["Daily kWh"] >= 3:
                st.warning(
                    f"High usage: {appliance['name']} consumes "
                    f"{appliance['Daily kWh']:.2f} kWh daily. "
                    "Consider reducing its usage."
                )
            elif appliance["Daily kWh"] > 0:
                st.success(
                    f"{appliance['name']}: Usage is relatively low "
                    "compared with the 3 kWh daily threshold."
                )

        st.info(
            "Tip: Switching off unused appliances and using "
            "energy-efficient devices can reduce electricity consumption."
        )
    else:
        st.info("Add appliances to receive recommendations.")

# ---------- ANALYTICS ----------
elif page == "Analytics":

    st.subheader("📊 Energy Analytics")

    if not df.empty:
        chart = px.pie(
            df,
            names="name",
            values="Monthly kWh",
            title="Monthly Energy Distribution"
        )
        st.plotly_chart(chart, use_container_width=True)

        st.metric("Estimated Monthly Bill", f"₹{monthly_bill:,.2f}")
        st.metric("Monthly Energy Usage", f"{monthly_units:.2f} kWh")
    else:
        st.info("Add appliances to view analytics.")

# ---------- SETTINGS ----------
elif page == "Settings":

    st.subheader("⚙️ Settings")

    st.write("Electricity tariff is currently set to ₹", tariff, "per unit.")
    st.write("One electricity unit = 1 kWh.")

    st.info(
        "This version uses estimated appliance consumption. "
        "Actual electricity bills may differ because of tariffs, "
        "fixed charges and real appliance operating patterns."
    )

st.sidebar.divider()
st.sidebar.caption("A23 Smart Home Agent | Prototype v1.0")
