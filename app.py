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
        st.write("Placeholder ready for Thembi's equipment parameters (Temp/Vibration thresholds).")

    elif selected_page == "Maintenance Data":
        st.subheader("🔧 Equipment Maintenance Monitoring")
        st.write("Placeholder ready for Thembi's availability calculations and maintenance tracking.")

    elif selected_page == "Generate Reports":
        st.subheader("📄 Generate Operational Reports")
        if st.button("Generate Summary Report"):
            st.success("Report compiled successfully.")

    elif selected_page == "Manage Users":
        st.subheader("⚙️ User Management Portal (Administrator Only)")
        st.text_input("New User ID")
        st.button("Grant Access")