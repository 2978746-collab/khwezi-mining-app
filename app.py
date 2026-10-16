import streamlit as st
import pandas as pd

# --- APP FRAMEWORK & LAYOUT SETUP ---
st.set_page_config(
    page_title="Khwezi Mining Monitoring Application",
    page_icon="⛏️",
    layout="wide"
)

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.session_state["role"] = ""

st.title("⛏️ Khwezi Mining Health, Safety & Equipment Monitoring Application")
st.markdown("*A centralized digital monitoring platform for operational decision-making.*")
st.divider()

# --- EQUIPMENT DATABASE AND MONITORING ---

equipment = pd.DataFrame({
    "Equipment_ID": ["TRK-001", "TRK-002", "DRL-001"],
    "Equipment_Type": ["Haul Truck", "Haul Truck", "Drill"],
    "Operating_Hours": [1250, 1680, 2300],
    "Temperature_C": [72, 85, 108],
    "Vibration_mm_s": [3.2, 5.7, 8.7],
    "Downtime_Hours": [25, 45, 140],
    "Maintenance_Status": ["Operational", "Due", "Overdue"]
})

def check_temperature(value):
    if value < 80:
        return "NORMAL"
    elif value <= 100:
        return "WARNING"
    else:
        return "CRITICAL"

def check_vibration(value):
    if value < 5:
        return "NORMAL"
    elif value <= 8:
        return "WARNING"
    else:
        return "CRITICAL"

def calculate_availability(operating_hours, downtime_hours):
    total = operating_hours + downtime_hours
    if total == 0:
        return 0.0
    return round(operating_hours / total * 100, 2)

def overall_condition(row):
    statuses = [row["Temperature_Status"], row["Vibration_Status"]]
    if "CRITICAL" in statuses:
        return "CRITICAL"
    elif "WARNING" in statuses:
        return "WARNING"
    return "NORMAL"

equipment["Temperature_Status"] = equipment["Temperature_C"].apply(check_temperature)
equipment["Vibration_Status"] = equipment["Vibration_mm_s"].apply(check_vibration)
equipment["Overall_Condition"] = equipment.apply(overall_condition, axis=1)
equipment["Availability_Percent"] = equipment.apply(
    lambda row: calculate_availability(
        row["Operating_Hours"], row["Downtime_Hours"]
    ),
    axis=1
)

# --- LOGIN PORTAL & RBAC (Section 3a & Table 1) ---
if not st.session_state["logged_in"]:
    st.subheader("🔒 User Access Control Portal")
    st.write("Please authenticate your credentials and select your operational role.")
    
    with st.form("login_form"):
        input_user = st.text_input("Username / Personnel ID")
        input_role = st.selectbox(
            "Select System Role:",
            ["Administrator", "Safety Officer", "Mining Engineer", "Maintenance Engineer", "Manager"]
        )
        login_button = st.form_submit_button("Authenticate & Enter")
        
        if login_button:
            if not input_user or input_user.strip() == "":
                st.error("⚠️ Error Prevention: Username cannot be empty.")
            else:
                st.session_state["logged_in"] = True
                st.session_state["username"] = input_user.strip()
                st.session_state["role"] = input_role
                st.rerun()

else:
    user = st.session_state["username"]
    role = st.session_state["role"]
    
    # --- SIDEBAR NAVIGATION & TABLE 1 PERMISSIONS ---
    st.sidebar.title("Navigation Menu")
    st.sidebar.write(f"**User:** {user}")
    st.sidebar.write(f"**Role:** {role}")
    st.sidebar.divider()
    
    allowed_pages = ["View Dashboard"]
    
    if role in ["Administrator", "Safety Officer", "Mining Engineer", "Manager"]:
        allowed_pages.extend(["Worker Safety Data", "Safety Incidents", "Risk Assessment"])
        
    if role in ["Administrator", "Mining Engineer", "Maintenance Engineer", "Manager"]:
        allowed_pages.extend(["Equipment Data", "Maintenance Data"])
        
    allowed_pages.append("Generate Reports")
    
    if role == "Administrator":
        allowed_pages.append("Manage Users")
        
    selected_page = st.sidebar.selectbox("Select Function", allowed_pages)
    
    st.sidebar.divider()
    if st.sidebar.button("Log Out"):
        st.session_state["logged_in"] = False
        st.rerun()

    # --- CENTRAL DASHBOARD & MODULE VIEWS ---
    if selected_page == "View Dashboard":
        st.subheader("📊 Central Monitoring Dashboard")
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total Workers", "142", "Active")
        k2.metric("Safety Incidents", "3", "-1 today", delta_color="inverse")
        k3.metric("Equipment Availability", "91.4%", "+2.1%")
        k4.metric("Critical Alerts", "2 Active", "Action Required", delta_color="inverse")
        st.info("💡 Use the sidebar navigation menu to access specific system modules.")

    elif selected_page == "Worker Safety Data":
        st.subheader("👷 Worker Health and Safety Monitoring")
        st.write("Placeholder ready for Sammie's worker safety database records.")

    elif selected_page == "Safety Incidents":
        st.subheader("🚨 Safety Incident Database")
        st.write("Placeholder ready for Sammie's safety incident tracking repository.")

    elif selected_page == "Risk Assessment":
        st.subheader("⚠️ Risk Assessment Matrix (Likelihood × Consequence)")
        l_val = st.slider("Likelihood (1-5)", 1, 5, 2)
        c_val = st.slider("Consequence (1-5)", 1, 5, 3)
        r_score = l_val * c_val
        st.write(f"Calculated Risk Score: **{r_score}**")
        if r_score <= 4: st.success("Low Risk")
        elif r_score <= 9: st.warning("Medium Risk")
        elif r_score <= 16: st.error("High Risk - Warning Triggered!")
        else: st.error("CRITICAL RISK - Immediate Action Required!")

    
    elif selected_page == "Equipment Data":
        st.subheader("🚜 Equipment Database & Condition Monitoring")

        st.dataframe(equipment, use_container_width=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Equipment", len(equipment))
        c2.metric("Critical Equipment", (equipment["Overall_Condition"] == "CRITICAL").sum())
        c3.metric("Average Availability", f"{equipment['Availability_Percent'].mean():.1f}%")

        selected_id = st.selectbox(
            "Select Equipment to Monitor",
            equipment["Equipment_ID"].tolist()
        )

        selected = equipment[equipment["Equipment_ID"] == selected_id].iloc[0]

        st.write(f"Temperature: {selected['Temperature_C']} °C — {selected['Temperature_Status']}")
        st.write(f"Vibration: {selected['Vibration_mm_s']} mm/s — {selected['Vibration_Status']}")

        if selected["Overall_Condition"] == "CRITICAL":
            st.error("CRITICAL: Equipment requires immediate attention!")
        elif selected["Overall_Condition"] == "WARNING":
            st.warning("WARNING: Equipment condition requires monitoring.")
        else:
            st.success("Equipment operating within normal limits.")


   
    elif selected_page == "Maintenance Data":
        st.subheader("🔧 Equipment Maintenance Monitoring")

        st.dataframe(
            equipment[[
                "Equipment_ID", "Operating_Hours", "Downtime_Hours",
                "Availability_Percent", "Maintenance_Status"
            ]],
            use_container_width=True
        )

        for _, item in equipment.iterrows():
            equipment_id = item["Equipment_ID"]
            status = item["Maintenance_Status"]
            availability = item["Availability_Percent"]
            downtime = item["Downtime_Hours"]

            if status in ["Overdue", "Under Maintenance"]:
                st.error(f"{equipment_id}: Maintenance status is {status}.")
            elif status == "Due":
                st.warning(f"{equipment_id}: Maintenance is due.")

            if availability < 90:
                st.warning(f"{equipment_id}: Low availability ({availability}%).")

            if downtime > 100:
                st.warning(f"{equipment_id}: Excessive downtime ({downtime} hours).")


    elif selected_page == "Generate Reports":
        st.subheader("📄 Generate Operational Reports")
        if st.button("Generate Summary Report"):
            st.success("Report compiled successfully.")

    elif selected_page == "Manage Users":
        st.subheader("⚙️ User Management Portal (Administrator Only)")
        st.text_input("New User ID")
        st.button("Grant Access")
