
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="A23 | Smart Home Agent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# DARK THEME DESIGN
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #080D18;
    color: #E5EAF5;
}

[data-testid="stSidebar"] {
    background: #101827;
    border-right: 1px solid #263449;
}

[data-testid="stSidebar"] h1 {
    color: #F1F5F9;
}

h1, h2, h3 {
    color: #F1F5F9 !important;
    font-weight: 700 !important;
}

p, label {
    color: #AAB7CC;
}

.hero {
    background: linear-gradient(115deg, #142C48, #102039, #172D43);
    border: 1px solid #254667;
    border-radius: 18px;
    padding: 27px;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 30px;
    margin: 0;
}

.hero p {
    color: #A9C4DE;
    margin-top: 9px;
}

.metric-card {
    background: linear-gradient(145deg, #172438, #111C2D);
    border: 1px solid #293B52;
    border-radius: 15px;
    padding: 19px;
    min-height: 125px;
}

.metric-label {
    color: #9EACC2;
    font-size: 13px;
    font-weight: 600;
}

.metric-value {
    color: #F1F5F9;
    font-size: 27px;
    font-weight: 800;
    margin-top: 12px;
}

.metric-note {
    color: #38BDF8;
    font-size: 12px;
    margin-top: 5px;
}

.device-card {
    background: #131F30;
    border: 1px solid #293B52;
    border-radius: 14px;
    padding: 17px;
    margin-bottom: 12px;
}

.device-name {
    color: #F1F5F9;
    font-size: 17px;
    font-weight: 700;
}

.device-info {
    color: #9EACC2;
    font-size: 13px;
    margin-top: 8px;
}

.section-note {
    background: #122B36;
    border-left: 4px solid #38BDF8;
    border-radius: 7px;
    padding: 13px;
    color: #C6E8F6;
    margin: 12px 0;
}

div.stButton > button {
    border-radius: 9px;
    font-weight: 600;
}

div[data-testid="stMetric"] {
    background: #172438;
    border: 1px solid #293B52;
    border-radius: 12px;
    padding: 15px;
}

div[data-testid="stMetric"] label {
    color: #9EACC2 !important;
}

hr {
    border-color: #263449;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION STATE
# =====================================================

if "appliances" not in st.session_state:
    st.session_state.appliances = [
        {"name": "Air Conditioner", "category": "Cooling",
         "watts": 1500.0, "hours": 6.0, "quantity": 1},
        {"name": "Refrigerator", "category": "Kitchen",
         "watts": 200.0, "hours": 12.0, "quantity": 1},
        {"name": "Ceiling Fan", "category": "Cooling",
         "watts": 75.0, "hours": 10.0, "quantity": 3},
        {"name": "LED Lights", "category": "Lighting",
         "watts": 12.0, "hours": 6.0, "quantity": 5}
    ]

if "tariff" not in st.session_state:
    st.session_state.tariff = 8.5

if "home_name" not in st.session_state:
    st.session_state.home_name = "My Smart Home"

# =====================================================
# DATA AND CALCULATIONS
# =====================================================

def get_dataframe():
    df = pd.DataFrame(st.session_state.appliances)

    if df.empty:
        return df

    df["Daily kWh"] = (
        df["watts"] * df["hours"] * df["quantity"] / 1000
    )

    df["Monthly kWh"] = df["Daily kWh"] * 30
    df["Monthly Cost"] = df["Monthly kWh"] * st.session_state.tariff

    return df


def money(value):
    return f"₹{value:,.2f}"


df = get_dataframe()

daily_units = df["Daily kWh"].sum() if not df.empty else 0
monthly_units = daily_units * 30
monthly_bill = monthly_units * st.session_state.tariff
yearly_bill = monthly_bill * 12

# =====================================================
# CHART THEME
# =====================================================

def style_chart(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#AAB7CC"),
        margin=dict(l=15, r=15, t=50, b=15),
        legend=dict(bgcolor="rgba(0,0,0,0)")
    )
    return fig


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:
    st.markdown("# ⚡ A23 SMART HOME")
    st.caption("ENERGY INTELLIGENCE PLATFORM")
    st.divider()

    page = st.radio(
        "MAIN MENU",
        [
            "Dashboard",
            "Appliances",
            "Energy Advisor",
            "Analytics",
            "Settings"
        ],
        label_visibility="visible"
    )

    st.divider()

    st.markdown("### Electricity tariff")

    st.number_input(
        "Price per unit (₹)",
        min_value=0.0,
        max_value=1000.0,
        step=0.5,
        key="tariff"
    )

    st.divider()

    st.caption("A23 SMART HOME AGENT")
    st.caption("Prototype V2.0")

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="hero">
    <h1>⚡ A23 Smart Home Agent</h1>
    <p>Intelligent Home Energy Monitoring & Optimization</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# DASHBOARD
# =====================================================

if page == "Dashboard":

    st.subheader("Overview")
    st.caption("Monitor your home's electricity performance.")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">DAILY CONSUMPTION</div>
            <div class="metric-value">{daily_units:.2f}</div>
            <div class="metric-note">kWh / day</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">MONTHLY CONSUMPTION</div>
            <div class="metric-value">{monthly_units:.2f}</div>
            <div class="metric-note">kWh / 30 days</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">ESTIMATED MONTHLY BILL</div>
            <div class="metric-value">{money(monthly_bill)}</div>
            <div class="metric-note">Based on your tariff</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">TOTAL APPLIANCES</div>
            <div class="metric-value">{len(df)}</div>
            <div class="metric-note">Registered devices</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    left, right = st.columns([1.6, 1])

    with left:
        st.subheader("Energy consumption")
        if not df.empty:
            fig = px.bar(
                df,
                x="name",
                y="Daily kWh",
                color="Daily kWh",
                color_continuous_scale=["#164E63", "#0EA5E9", "#7DD3FC"],
                title="Daily usage by appliance",
                labels={"name": "Appliance", "Daily kWh": "kWh"}
            )
            fig.update_layout(showlegend=False)
            style_chart(fig)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Add appliances to see consumption.")

    with right:
        st.subheader("Energy distribution")
        if not df.empty:
            fig = px.pie(
                df,
                names="name",
                values="Daily kWh",
                hole=0.65,
                color_discrete_sequence=[
                    "#0EA5E9", "#38BDF8", "#6366F1",
                    "#14B8A6", "#F59E0B"
                ]
            )
            style_chart(fig)
            st.plotly_chart(fig, use_container_width=True)

    st.subheader("Appliance summary")

    if not df.empty:
        display = df[[
            "name", "watts", "hours", "quantity",
            "Daily kWh", "Monthly Cost"
        ]].copy()

        display.columns = [
            "Appliance", "Power (W)", "Hours/day",
            "Quantity", "Daily kWh", "Monthly Cost (₹)"
        ]

        st.dataframe(
            display,
            use_container_width=True,
            hide_index=True
        )

    st.caption(
        "Estimates use entered power ratings and daily operating hours. "
        "Actual consumption may differ."
    )

# =====================================================
# APPLIANCE MANAGEMENT
# =====================================================

elif page == "Appliances":

    st.subheader("Appliance Management")
    st.caption("Add and manage the electrical devices in your home.")

    with st.expander("＋ Add a new appliance", expanded=True):

        with st.form("add_appliance_form", clear_on_submit=True):

            name = st.text_input("Appliance name")

            category = st.selectbox(
                "Category",
                ["Cooling", "Kitchen", "Lighting",
                 "Entertainment", "Other"]
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                watts = st.number_input(
                    "Power rating (Watts)",
                    min_value=1.0,
                    max_value=50000.0,
                    value=100.0
                )

            with col2:
                hours = st.number_input(
                    "Hours used daily",
                    min_value=0.0,
                    max_value=24.0,
                    value=5.0
                )

            with col3:
                quantity = st.number_input(
                    "Quantity",
                    min_value=1,
                    max_value=100,
                    value=1
                )

            submitted = st.form_submit_button(
                "Add appliance",
                use_container_width=True
            )

            if submitted:
                if name.strip():
                    st.session_state.appliances.append({
                        "name": name.strip(),
                        "category": category,
                        "watts": watts,
                        "hours": hours,
                        "quantity": quantity
                    })
                    st.success(f"{name} added successfully!")
                    st.rerun()
                else:
                    st.error("Enter an appliance name.")

    st.divider()
    st.subheader("Your registered appliances")

    if not df.empty:

        for i, appliance in enumerate(st.session_state.appliances):

            device_col, delete_col = st.columns([5, 1])

            consumption = (
                appliance["watts"]
                * appliance["hours"]
                * appliance["quantity"] / 1000
            )

            with device_col:
                st.markdown(f"""
                <div class="device-card">
                    <div class="device-name">
                        ⚡ {appliance['name']}
                    </div>
                    <div class="device-info">
                        {appliance['category']} &nbsp;|&nbsp;
                        {appliance['watts']:.0f} W &nbsp;|&nbsp;
                        {appliance['hours']:.1f} hours/day
                        &nbsp;|&nbsp; Quantity: {appliance['quantity']}
                    </div>
                    <div class="metric-note">
                        {consumption:.2f} kWh daily
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with delete_col:
                st.write("")
                if st.button("🗑️", key=f"delete_{i}"):
                    st.session_state.appliances.pop(i)
                    st.rerun()

    else:
        st.info("No appliances registered. Add your first appliance.")

# =====================================================
# ENERGY ADVISOR
# =====================================================

elif page == "Energy Advisor":

    st.subheader("🤖 Smart Energy Advisor")
    st.caption("Recommendations based on your appliance consumption.")

    if df.empty:
        st.info("Add appliances to generate recommendations.")

    else:

        total = df["Daily kWh"].sum()

        st.metric("Total daily consumption", f"{total:.2f} kWh")

        st.markdown("### Energy recommendations")

        recommendations = []

        for _, appliance in df.iterrows():

            if appliance["Daily kWh"] >= 3:
                recommendations.append((
                    "High consumption",
                    appliance["name"],
                    appliance["Daily kWh"],
                    "Review operating hours and energy efficiency."
                ))

            if appliance["hours"] >= 10:
                recommendations.append((
                    "Long operating time",
                    appliance["name"],
                    appliance["Daily kWh"],
                    "Check whether its daily operating schedule can be optimized."
                ))

        if recommendations:
            for title, name, usage, advice in recommendations:
                st.warning(
                    f"**{title}: {name}** — "
                    f"{usage:.2f} kWh/day. {advice}"
                )
        else:
            st.success("No appliances crossed the current advisory thresholds.")

        st.markdown("### Potential savings simulation")

        reduction = st.slider(
            "Assumed reduction in appliance operating hours (%)",
            min_value=0,
            max_value=50,
            value=10,
            step=5
        )

        possible_daily = total * reduction / 100
        possible_monthly = possible_daily * 30
        possible_savings = possible_monthly * st.session_state.tariff

        a, b, c = st.columns(3)

        a.metric("Potential daily savings", f"{possible_daily:.2f} kWh")
        b.metric("Potential monthly savings", f"{possible_monthly:.2f} kWh")
        c.metric("Potential bill savings", money(possible_savings))

        st.caption(
            "Illustrative scenario only. Assumes the selected reduction "
            "applies uniformly to all appliances. It is not a measured or "
            "guaranteed saving."
        )

# =====================================================
# ANALYTICS
# =====================================================

elif page == "Analytics":

    st.subheader("Energy Analytics")
    st.caption("Explore your estimated electricity consumption.")

    if df.empty:
        st.info("Add appliances to generate analytics.")

    else:

        col1, col2 = st.columns(2)

        with col1:
            fig = px.bar(
                df,
                x="name",
                y="Monthly kWh",
                color="Monthly kWh",
                color_continuous_scale=["#164E63", "#0EA5E9", "#7DD3FC"],
                title="Monthly appliance consumption"
            )
            fig.update_layout(showlegend=False)
            style_chart(fig)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.pie(
                df,
                names="name",
                values="Monthly Cost",
                hole=0.6,
                title="Estimated monthly bill distribution",
                color_discrete_sequence=[
                    "#0EA5E9", "#38BDF8", "#6366F1",
                    "#14B8A6", "#F59E0B"
                ]
            )
            style_chart(fig)
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Consumption report")

        r1, r2, r3 = st.columns(3)

        r1.metric("Monthly units", f"{monthly_units:.2f} kWh")
        r2.metric("Monthly cost", money(monthly_bill))
        r3.metric("Yearly cost estimate", money(yearly_bill))

        st.markdown("### Appliance cost ranking")

        ranked = df.sort_values(
            "Monthly Cost", ascending=False
        )

        for _, appliance in ranked.iterrows():
            st.write(
                f"**{appliance['name']}** — "
                f"{money(appliance['Monthly Cost'])} / month"
            )

            st.progress(
                min(
                    float(appliance["Monthly Cost"] /
                          monthly_bill) if monthly_bill > 0 else 0,
                    1.0
                )
            )

# =====================================================
# SETTINGS
# =====================================================

elif page == "Settings":

    st.subheader("Settings")
    st.caption("Configure your smart home energy profile.")

    st.markdown("### Home profile")

    home_name = st.text_input(
        "Home name",
        value=st.session_state.home_name
    )

    if st.button("Save home profile"):
        st.session_state.home_name = home_name
        st.success("Home profile updated.")

    st.divider()

    st.markdown("### Electricity settings")

    st.write(
        f"Current tariff: ₹{st.session_state.tariff:.2f} per unit"
    )

    st.info(
        "One electricity unit is equivalent to one kilowatt-hour (kWh). "
        "Actual electricity bills may also include fixed charges, taxes "
        "and slab-based tariffs."
    )

    st.divider()

    st.markdown("### Application information")

    st.write("Application: A23 Smart Home Agent")
    st.write("Version: 2.0")
    st.write("Framework: Streamlit")
    st.write("Analytics: Pandas and Plotly")

    st.warning(
        "This is a software prototype using user-entered appliance data. "
        "It does not currently connect to physical smart-home devices."
    )

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.markdown(
    "<div style='text-align:center;color:#718096;padding:15px;'>"
    "⚡ A23 Smart Home Agent · Version 2.0 · "
    "Intelligent Energy Management"
    "</div>",
    unsafe_allow_html=True
)
