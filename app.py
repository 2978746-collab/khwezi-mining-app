import streamlit as st
import pandas as pd

# --- PHASE 1: APP FRAMEWORK & LAYOUT SETUP ---
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

# --- THEMBI'S BACK-END LOGIC: EQUIPMENT DATABASE & MONITORING ---
# Using the fallback dataframe so it won't crash if equipment.csv is missing
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
    if value < 80: return "NORMAL"
    elif value <= 100: return "WARNING"
    else: return "CRITICAL"

def check_vibration(value):
    if value < 5: return "NORMAL"
    elif value <= 8: return "WARNING"
    else: return "CRITICAL"

def calculate_availability(operating_hours, downtime_hours):
    total = operating_hours + downtime_hours
    if total == 0: return 0.0
    return round(operating_hours / total * 100, 2)

def overall_condition(row):
    statuses = [row["Temperature_Status"], row["Vibration_Status"]]
    if "CRITICAL" in statuses: return "CRITICAL"
    elif "WARNING" in statuses: return "WARNING"
    return "NORMAL"

equipment["Temperature_Status"] = equipment["Temperature_C"].apply(check_temperature)
equipment["Vibration_Status"] = equipment["Vibration_mm_s"].apply(check_vibration)
equipment["Overall_Condition"] = equipment.apply(overall_condition, axis=1)
equipment["Availability_Percent"] = equipment.apply(
    lambda row: calculate_availability(row["Operating_Hours"], row["Downtime_Hours"]), axis=1
)

# --- TSHEGO'S FRONT-END: LOGIN PORTAL & RBAC (Section 3a & Table 1) ---
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
    
    # --- TSHEGO'S SIDEBAR NAVIGATION & TABLE 1 PERMISSIONS ---
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

    # --- CENTRAL DASHBOARD ---
    if selected_page == "View Dashboard":
        st.subheader("📊 Central Monitoring Dashboard")
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total Workers", "142", "Active")
        k2.metric("Safety Incidents", "3", "-1 today", delta_color="inverse")
        k3.metric("Equipment Availability", f"{equipment['Availability_Percent'].mean():.1f}%")
        k4.metric("Critical Alerts", (equipment["Overall_Condition"] == "CRITICAL").sum(), "Action Required", delta_color="inverse")
        st.info("💡 Use the sidebar navigation menu to access specific system modules.")

    # --- SAMMIE'S PLACEHOLDERS ---
    elif selected_page == "Worker Safety Data":
        st.subheader("👷 Worker Health and Safety Monitoring")
        
def create_file():
    """Create the CSV file if it does not already exist."""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow([
                "Worker_ID",
                "Department",
                "Job_Role",
                "Shift",
                "PPE_Compliance",
                "Safety_Training",
                "Fatigue_Level",
                "Safety_Observations",
                "Near_Misses",
                "Previous_Incidents",
                "Risk_Level"
            ])


def assess_worker_risk(ppe, training, fatigue,
                       observations, near_misses, incidents):
    """Identify potentially unsafe worker conditions."""

    warnings = []

    if ppe.lower() == "no":
        warnings.append("Worker is not complying with PPE requirements.")

    if training.lower() == "no":
        warnings.append("Worker has not completed safety training.")

    if fatigue >= 4:
        warnings.append("High fatigue level detected.")

    if observations >= 3:
        warnings.append("Multiple safety observations recorded.")

    if near_misses > 0:
        warnings.append("Near-miss incidents have been reported.")

    if incidents > 0:
        warnings.append("Previous safety incidents recorded.")

    # Determine the overall risk level.
    if ppe.lower() == "no" or fatigue == 5:
        risk_level = "Critical"

    elif training.lower() == "no" or fatigue >= 4:
        risk_level = "High"

    elif observations >= 3 or near_misses > 0 or incidents > 0:
        risk_level = "Medium"

    else:
        risk_level = "Low"

    return risk_level, warnings


def add_worker():
    """Collect worker information and save it."""

    print("\n--- Worker Safety Registration ---")

    worker_id = input("Enter Worker ID: ").strip()
    department = input("Enter Department: ").strip()
    job_role = input("Enter Job Role: ").strip()

    shift = input("Enter Shift (Day/Night): ").strip().title()

    while shift not in ["Day", "Night"]:
        print("Invalid shift. Enter Day or Night.")
        shift = input("Enter Shift: ").strip().title()

    ppe = input("Is the worker complying with PPE? (Yes/No): ")
    while ppe.lower() not in ["yes", "no"]:
        ppe = input("Enter Yes or No: ")

    training = input("Has safety training been completed? (Yes/No): ")
    while training.lower() not in ["yes", "no"]:
        training = input("Enter Yes or No: ")

    fatigue = int(input("Enter fatigue level (1-5): "))
    while fatigue < 1 or fatigue > 5:
        print("Fatigue must be between 1 and 5.")
        fatigue = int(input("Enter fatigue level (1-5): "))

    observations = int(input("Number of safety observations: "))
    near_misses = int(input("Number of near misses: "))
    incidents = int(input("Number of previous incidents: "))

    if observations < 0 or near_misses < 0 or incidents < 0:
        print("Counts cannot be negative.")
        return

    risk_level, warnings = assess_worker_risk(
        ppe,
        training,
        fatigue,
        observations,
        near_misses,
        incidents
    )

    # Save the worker's information.
    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            worker_id,
            department,
            job_role,
            shift,
            ppe.title(),
            training.title(),
            fatigue,
            observations,
            near_misses,
            incidents,
            risk_level
        ])

    print("\nWorker information saved successfully.")
    print("Worker risk level:", risk_level)

    if warnings:
        print("\nSAFETY WARNINGS:")

        for warning in warnings:
            print("-", warning)

    else:
        print("No unsafe conditions identified.")


def view_workers():
    """Display all registered workers."""

    with open(FILE_NAME, "r", newline="") as file:
        reader = csv.reader(file)

        for row in reader:
            print(row)


def main():
    create_file()

    while True:
        print("\n=== WORKER SAFETY MONITORING ===")
        print("1. Register worker")
        print("2. View worker records")
        print("3. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            add_worker()

        elif choice == "2":
            view_workers()

        elif choice == "3":
            print("Exiting worker safety monitoring.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

    elif selected_page == "Safety Incidents":
        st.subheader("🚨 Safety Incident Database")
        FILE_NAME = "safety_incidents.csv"

FIELDS = [
    "Incident_ID",
    "Date",
    "Time",
    "Shift",
    "Location",
    "Department",
    "Incident_Type",
    "Severity",
    "Injury_Status",
    "Lost_Time_Injury",
    "Cause",
    "Corrective_Action",
    "Incident_Status"
]


def create_file():
    """Create the incident database if necessary."""

    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()


def load_incidents():
    """Load all incident records from the CSV file."""

    with open(FILE_NAME, "r", newline="") as file:
        return list(csv.DictReader(file))


def add_incident():
    """Record a new safety incident."""

    print("\n--- Add Safety Incident ---")

    incidents = load_incidents()

    incident_id = input("Enter Incident ID: ").strip()

    if not incident_id:
        print("Incident ID cannot be empty.")
        return

    if any(row["Incident_ID"] == incident_id for row in incidents):
        print("This Incident ID already exists.")
        return

    date = input("Enter date (YYYY-MM-DD): ").strip()

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format.")
        return

    time = input("Enter time (HH:MM): ").strip()

    try:
        datetime.strptime(time, "%H:%M")
    except ValueError:
        print("Invalid time format.")
        return

    shift = input("Enter shift (Day/Night): ").strip().title()

    if shift not in ["Day", "Night"]:
        print("Invalid shift.")
        return

    location = input("Enter incident location: ").strip()
    department = input("Enter department: ").strip()

    incident_type = input(
        "Enter incident type (e.g. fall, machinery, fire, near miss): "
    ).strip()

    severity = input(
        "Enter severity (Low/Medium/High/Critical): "
    ).strip().title()

    if severity not in ["Low", "Medium", "High", "Critical"]:
        print("Invalid severity.")
        return

    injury_status = input(
        "Was there an injury? (Yes/No): "
    ).strip().title()

    if injury_status not in ["Yes", "No"]:
        print("Enter Yes or No.")
        return

    lti = input(
        "Was it a lost-time injury? (Yes/No): "
    ).strip().title()

    if lti not in ["Yes", "No"]:
        print("Enter Yes or No.")
        return

    cause = input("Enter cause of incident: ").strip()

    corrective_action = input(
        "Enter corrective action: "
    ).strip()

    incident_status = input(
        "Enter status (Open/Under Investigation/Closed): "
    ).strip().title()

    valid_statuses = [
        "Open",
        "Under Investigation",
        "Closed"
    ]

    if incident_status not in valid_statuses:
        print("Invalid incident status.")
        return

    record = {
        "Incident_ID": incident_id,
        "Date": date,
        "Time": time,
        "Shift": shift,
        "Location": location,
        "Department": department,
        "Incident_Type": incident_type,
        "Severity": severity,
        "Injury_Status": injury_status,
        "Lost_Time_Injury": lti,
        "Cause": cause,
        "Corrective_Action": corrective_action,
        "Incident_Status": incident_status
    }

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writerow(record)

    print("Incident recorded successfully.")

    if severity in ["High", "Critical"]:
        print("WARNING: High-severity incident requires attention.")


def view_incidents():
    """Display all incidents."""

    incidents = load_incidents()

    if not incidents:
        print("No incidents have been recorded.")
        return

    for incident in incidents:
        print(incident)


def search_incident():
    """Search for an incident by its ID."""

    incident_id = input("Enter Incident ID to search: ").strip()

    incidents = load_incidents()

    for incident in incidents:
        if incident["Incident_ID"] == incident_id:
            print("\nIncident found:")
            print(incident)
            return

    print("Incident not found.")


def filter_incidents():
    """Filter incidents by department, shift or severity."""

    incidents = load_incidents()

    if not incidents:
        print("No incident records available.")
        return

    print("Filter by:")
    print("1. Department")
    print("2. Shift")
    print("3. Severity")

    choice = input("Select filter: ")

    if choice == "1":
        field = "Department"
        value = input("Enter department: ").strip().lower()

    elif choice == "2":
        field = "Shift"
        value = input("Enter shift: ").strip().lower()

    elif choice == "3":
        field = "Severity"
        value = input("Enter severity: ").strip().lower()

    else:
        print("Invalid choice.")
        return

    results = [
        incident for incident in incidents
        if incident[field].lower() == value
    ]

    print("\nFiltered incidents:")

    if results:
        for incident in results:
            print(incident)
    else:
        print("No matching incidents found.")


def analyse_incidents():
    """Count incidents and analyse basic trends."""

    incidents = load_incidents()

    if not incidents:
        print("No incidents available for analysis.")
        return

    print("\nTotal incidents:", len(incidents))

    severity_counts = Counter(
        incident["Severity"] for incident in incidents
    )

    department_counts = Counter(
        incident["Department"] for incident in incidents
    )

    shift_counts = Counter(
        incident["Shift"] for incident in incidents
    )

    type_counts = Counter(
        incident["Incident_Type"] for incident in incidents
    )

    total_near_misses = sum(
        1 for incident in incidents
        if "near miss" in incident["Incident_Type"].lower()
    )

    high_critical = sum(
        1 for incident in incidents
        if incident["Severity"] in ["High", "Critical"]
    )

    lost_time_injuries = sum(
        1 for incident in incidents
        if incident["Lost_Time_Injury"] == "Yes"
    )

    print("\nIncidents by severity:", dict(severity_counts))
    print("Incidents by department:", dict(department_counts))
    print("Incidents by shift:", dict(shift_counts))
    print("Incidents by type:", dict(type_counts))
    print("Total near misses:", total_near_misses)
    print("High/Critical incidents:", high_critical)
    print("Lost-time injuries:", lost_time_injuries)

    print("\nMonthly incident trends:")

    monthly_counts = Counter(
        incident["Date"][:7] for incident in incidents
    )

    for month, count in sorted(monthly_counts.items()):
        print(month, ":", count, "incident(s)")


def main():
    create_file()

    while True:
        print("\n=== SAFETY INCIDENT DATABASE ===")
        print("1. Add incident")
        print("2. View incidents")
        print("3. Search incident")
        print("4. Filter incidents")
        print("5. Analyse incidents")
        print("6. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            add_incident()

        elif choice == "2":
            view_incidents()

        elif choice == "3":
            search_incident()

        elif choice == "4":
            filter_incidents()

        elif choice == "5":
            analyse_incidents()

        elif choice == "6":
            print("Exiting incident database.")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()

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

    # --- THEMBI'S INTEGRATED MODULES ---
    elif selected_page == "Equipment Data":
        st.subheader("🚜 Equipment Database & Condition Monitoring")
        st.dataframe(equipment, use_container_width=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Equipment", len(equipment))
        c2.metric("Critical Equipment", (equipment["Overall_Condition"] == "CRITICAL").sum())
        c3.metric("Average Availability", f"{equipment['Availability_Percent'].mean():.1f}%")

        selected_id = st.selectbox("Select Equipment to Monitor", equipment["Equipment_ID"].tolist())
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
            equipment[["Equipment_ID", "Operating_Hours", "Downtime_Hours", "Availability_Percent", "Maintenance_Status"]],
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

    # --- ADMIN / REPORTS ---
    elif selected_page == "Generate Reports":
        st.subheader("📄 Generate Operational Reports")
        if st.button("Generate Summary Report"):
            st.success("Report compiled successfully.")

    elif selected_page == "Manage Users":
        st.subheader("⚙️ User Management Portal (Administrator Only)")
        st.text_input("New User ID")
        st.button("Grant Access")
