"""
app.py - Main Streamlit Application for CareConnect
FIT-FEST 2026 Hackathon | Flora Institute of Technology, Pune
Clinic Appointment & Emergency Coordination System
"""

import streamlit as st
from datetime import date, datetime
import database as db

# ==============================================================================
# PAGE CONFIGURATION & STYLING
# ==============================================================================
st.set_page_config(
    page_title="CareConnect - Clinic & Emergency Hub",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom minimal CSS for clean medical aesthetic
st.markdown("""
<style>
    .main-header {
        font-size: 2.1rem;
        font-weight: 700;
        color: #0E7490;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.2rem;
    }
    .disclaimer-card {
        background-color: #FEF3C7;
        border-left: 5px solid #F59E0B;
        padding: 10px 15px;
        border-radius: 4px;
        color: #92400E;
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
    }
    .emergency-card {
        background-color: #FEE2E2;
        border-left: 5px solid #EF4444;
        padding: 12px 18px;
        border-radius: 4px;
        color: #991B1B;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Ensure database and tables exist at startup
db.init_db()


# ==============================================================================
# SIDEBAR NAVIGATION & DISCLAIMERS
# ==============================================================================
with st.sidebar:
    st.markdown("## 🏥 CareConnect")
    st.caption("Clinic Appointment & Emergency Coordination System")
    st.markdown("---")

    menu_selection = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "👤 Patient Registration",
            "📅 Book Appointment",
            "📋 Manage Appointments",
            "🚑 Emergency Coordination",
            "🩸 Blood Bank Directory",
            "ℹ️ About & Disclaimers"
        ]
    )

    st.markdown("---")
    st.markdown("### 📞 National Helplines")
    st.markdown("🚑 **Ambulance**: `108`")
    st.markdown("🚨 **Emergency**: `112`")
    st.markdown("🩸 **Blood Helpline**: `104`")

    st.markdown("---")
    st.caption("FIT-FEST 2026 Hackathon | Pune\nBuilt with Python & Streamlit")


# ==============================================================================
# GLOBAL NOTICE (Medical Boundary & Simulated Data Notice)
# ==============================================================================
st.markdown("""
<div class="disclaimer-card">
    <strong>⚠️ Important Hackathon Disclaimer:</strong> CareConnect is strictly an <strong>administrative and emergency coordination tool</strong>. 
    It does <strong>NOT</strong> provide medical diagnosis, clinical advice, or treatment decisions. 
    All ambulance logs and blood availability figures are <strong>simulated demo data</strong> for demonstration purposes.
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# 1. 🏠 DASHBOARD
# ==============================================================================
if menu_selection == "🏠 Dashboard":
    st.markdown('<div class="main-header">🏥 CareConnect Overview Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Real-time administrative metrics and emergency response status</div>', unsafe_allow_html=True)

    metrics = db.get_dashboard_metrics()

    # Metric Cards Row
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric(label="👥 Registered Patients", value=metrics["total_patients"])
    with col2:
        st.metric(label="📅 Today's Appointments", value=metrics["today_appointments"])
    with col3:
        st.metric(label="⏳ Scheduled Visits", value=metrics["pending_appointments"])
    with col4:
        st.metric(label="🚨 Pending Emergencies", value=metrics["active_emergencies"])
    with col5:
        st.metric(label="🩸 Blood Units (Simulated)", value=metrics["total_blood_units"])

    st.markdown("---")

    # Today's Appointments Preview
    st.subheader("📅 Today's Clinic Appointments")
    today_iso = date.today().isoformat()
    today_df = db.get_all_appointments(filter_date=today_iso)

    if not today_df.empty:
        display_df = today_df[["appointment_id", "patient_name", "doctor_name", "department", "appointment_time", "status", "reason"]]
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("No appointments scheduled for today yet. Use the 'Book Appointment' page to schedule a visit.")

    # Recent Emergency Requests Alert Box
    if metrics["active_emergencies"] > 0:
        st.markdown("""
        <div class="emergency-card">
            <strong>🚨 Alert:</strong> There are active emergency requests awaiting dispatch coordination in the queue!
            Check the <strong>Emergency Coordination</strong> tab for details.
        </div>
        """, unsafe_allow_html=True)


# ==============================================================================
# 2. 👤 PATIENT REGISTRATION
# ==============================================================================
elif menu_selection == "👤 Patient Registration":
    st.markdown('<div class="main-header">👤 Patient Registration</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Register new patients into the clinic database with zero paper clutter</div>', unsafe_allow_html=True)

    with st.form("patient_registration_form", clear_on_submit=True):
        st.subheader("Patient Details Form")
        col_a, col_b = st.columns(2)

        with col_a:
            full_name = st.text_input("Full Name *", placeholder="e.g. Ramesh Kulkarni")
            age = st.number_input("Age *", min_value=1, max_value=120, value=25)
            gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
            phone = st.text_input("Phone Number (10 digits) *", placeholder="e.g. 9823012345")

        with col_b:
            email = st.text_input("Email Address (Optional)", placeholder="e.g. ramesh@example.com")
            blood_group = st.selectbox("Blood Group *", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            city = st.text_input("City / Area *", value="Pune")

        submitted = st.form_submit_button("💾 Register Patient", use_container_width=True)

        if submitted:
            if not full_name.strip():
                st.error("Please enter the patient's full name.")
            elif not phone.strip() or len(phone.strip()) < 10:
                st.error("Please provide a valid 10-digit phone number.")
            else:
                new_patient_id = db.add_patient(
                    full_name=full_name,
                    age=int(age),
                    gender=gender,
                    phone=phone,
                    email=email,
                    blood_group=blood_group,
                    city=city
                )
                st.success(f"✅ Patient '{full_name}' registered successfully! Assigned Patient ID: #{new_patient_id}")

    st.markdown("---")
    st.subheader("📋 Registered Patients Directory")
    patients_df = db.get_all_patients()
    if not patients_df.empty:
        st.dataframe(patients_df, use_container_width=True, hide_index=True)
    else:
        st.info("No patients registered yet.")


# ==============================================================================
# 3. 📅 BOOK APPOINTMENT
# ==============================================================================
elif menu_selection == "📅 Book Appointment":
    st.markdown('<div class="main-header">📅 Schedule a Clinic Appointment</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Select a registered patient, doctor, and convenient time slot</div>', unsafe_allow_html=True)

    patient_options = db.get_patient_dropdown_options()

    if not patient_options:
        st.warning("⚠️ No registered patients found in the system. Please register a patient first.")
    else:
        with st.form("book_appointment_form", clear_on_submit=True):
            col_1, col_2 = st.columns(2)

            with col_1:
                selected_label = st.selectbox("Select Registered Patient *", list(patient_options.keys()))
                patient_id = patient_options[selected_label]

                doctor_choice = st.selectbox(
                    "Select Doctor & Department *",
                    [
                        "Dr. Sunita Kulkarni — General Medicine",
                        "Dr. Anand Mehta — Cardiology",
                        "Dr. Rajesh Shinde — Orthopedics",
                        "Dr. Meera Joshi — Pediatrics",
                        "Dr. Amit Deshpande — ENT",
                        "Dr. Pooja Sawant — Dermatology"
                    ]
                )
                doctor_name, department = [x.strip() for x in doctor_choice.split("—")]

            with col_2:
                appointment_date = st.date_input("Appointment Date *", min_value=date.today())
                appointment_time = st.selectbox(
                    "Preferred Time Slot *",
                    [
                        "09:00 AM", "09:30 AM", "10:00 AM", "10:30 AM",
                        "11:00 AM", "11:30 AM", "02:00 PM", "02:30 PM",
                        "03:00 PM", "03:30 PM", "04:00 PM", "04:30 PM"
                    ]
                )
                reason = st.text_input("Reason for Visit / Symptoms *", placeholder="e.g. Mild fever and body ache")

            book_submitted = st.form_submit_button("📅 Confirm & Schedule Appointment", use_container_width=True)

            if book_submitted:
                if not reason.strip():
                    st.error("Please enter the reason for the visit.")
                else:
                    new_apt_id = db.add_appointment(
                        patient_id=patient_id,
                        doctor_name=doctor_name,
                        department=department,
                        appointment_date=appointment_date.isoformat(),
                        appointment_time=appointment_time,
                        reason=reason
                    )
                    st.success(f"✅ Appointment #{new_apt_id} successfully scheduled with {doctor_name} on {appointment_date} at {appointment_time}!")


# ==============================================================================
# 4. 📋 MANAGE APPOINTMENTS
# ==============================================================================
elif menu_selection == "📋 Manage Appointments":
    st.markdown('<div class="main-header">📋 Manage Appointments</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">View schedule, filter by status, and update visit progress</div>', unsafe_allow_html=True)

    filter_col1, filter_col2 = st.columns([1, 1])
    with filter_col1:
        status_filter = st.selectbox("Filter by Status", ["All", "Scheduled", "Completed", "Cancelled"])
    with filter_col2:
        date_filter_enabled = st.checkbox("Filter by specific date")
        selected_date = st.date_input("Date", value=date.today()) if date_filter_enabled else None

    date_str = selected_date.isoformat() if date_filter_enabled else None
    appointments_df = db.get_all_appointments(filter_status=status_filter, filter_date=date_str)

    if appointments_df.empty:
        st.info("No appointments found matching the selected filter.")
    else:
        st.dataframe(appointments_df, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.subheader("🔄 Update Appointment Status")

        # Interactive status changer
        col_up1, col_up2, col_up3 = st.columns([2, 1, 1])
        with col_up1:
            apt_options = {
                f"Appointment #{row['appointment_id']} - {row['patient_name']} ({row['appointment_date']} @ {row['appointment_time']}) [{row['status']}]": row['appointment_id']
                for _, row in appointments_df.iterrows()
            }
            selected_apt_label = st.selectbox("Select Appointment to Update", list(apt_options.keys()))
            selected_apt_id = apt_options[selected_apt_label]

        with col_up2:
            new_status = st.selectbox("New Status", ["Completed", "Cancelled", "Scheduled"])

        with col_up3:
            st.write("") # spacing
            st.write("")
            if st.button("Update Status", use_container_width=True):
                db.update_appointment_status(selected_apt_id, new_status)
                st.success(f"Appointment #{selected_apt_id} status updated to '{new_status}'!")
                st.rerun()


# ==============================================================================
# 5. 🚑 EMERGENCY & AMBULANCE COORDINATION
# ==============================================================================
elif menu_selection == "🚑 Emergency Coordination":
    st.markdown('<div class="main-header">🚑 Emergency & Ambulance Coordination</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Log urgent requests, triage priority, and coordinate ambulance dispatch</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="emergency-card">
        <strong>🚨 SIMULATED EMERGENCY DISPATCH LOG (DEMO ONLY)</strong><br>
        In an actual life-threatening medical emergency, call <strong>108</strong> (Ambulance) or <strong>112</strong> (National Emergency Service) immediately.
    </div>
    """, unsafe_allow_html=True)

    with st.expander("➕ Log New Emergency / Ambulance Request", expanded=True):
        with st.form("emergency_request_form", clear_on_submit=True):
            col_e1, col_e2 = st.columns(2)

            with col_e1:
                caller_name = st.text_input("Caller / Attendant Name *", placeholder="e.g. Ramesh Gaikwad")
                contact_number = st.text_input("Contact Phone Number *", placeholder="e.g. 9822011223")
                urgency = st.selectbox("Urgency Priority Triage *", ["Critical (Immediate)", "Moderate (Urgent)", "Non-Critical (Routine Transfer)"])

            with col_e2:
                pickup_address = st.text_area("Pickup Address & Landmark *", placeholder="e.g. Building C, Swargate, Pune")
                emergency_notes = st.text_area("Patient Condition / Notes *", placeholder="e.g. Elderly person experiencing breathing difficulty")

            submitted_emergency = st.form_submit_button("🚨 Dispatch Ambulance Request", use_container_width=True)

            if submitted_emergency:
                if not caller_name.strip() or not contact_number.strip() or not pickup_address.strip():
                    st.error("Please fill in the caller name, phone number, and pickup address.")
                else:
                    urgency_clean = urgency.split()[0]
                    new_req_id = db.add_emergency_request(
                        caller_name=caller_name,
                        contact_number=contact_number,
                        pickup_address=pickup_address,
                        urgency_level=urgency_clean,
                        notes=emergency_notes
                    )
                    st.success(f"🚨 Emergency Request #{new_req_id} logged into dispatch queue! Status: PENDING")

    st.markdown("---")
    st.subheader("📋 Active Emergency & Ambulance Requests")
    emergencies_df = db.get_all_emergency_requests()

    if not emergencies_df.empty:
        st.dataframe(emergencies_df, use_container_width=True, hide_index=True)

        st.markdown("#### Update Dispatch Status")
        em_col1, em_col2, em_col3 = st.columns([2, 1, 1])
        with em_col1:
            em_options = {
                f"Emergency #{r['id']} - Caller: {r['caller_name']} ({r['urgency_level']}) [{r['status']}]": r['id']
                for _, r in emergencies_df.iterrows()
            }
            selected_em_label = st.selectbox("Select Emergency Request", list(em_options.keys()))
            selected_em_id = em_options[selected_em_label]

        with em_col2:
            new_em_status = st.selectbox("Dispatch Status", ["Dispatched", "Resolved", "Pending"])

        with em_col3:
            st.write("")
            st.write("")
            if st.button("Update Dispatch", use_container_width=True):
                db.update_emergency_status(selected_em_id, new_em_status)
                st.success(f"Emergency #{selected_em_id} status updated to '{new_em_status}'!")
                st.rerun()
    else:
        st.info("No active emergency requests in the queue.")


# ==============================================================================
# 6. 🩸 BLOOD BANK DIRECTORY
# ==============================================================================
elif menu_selection == "🩸 Blood Bank Directory":
    st.markdown('<div class="main-header">🩸 Blood Bank & Availability Directory</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Search Pune hospitals and blood banks for available blood group units</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="disclaimer-card">
        <strong>ℹ️ Notice:</strong> Blood availability data shown below is <strong>simulated demonstration data</strong> for the Pune region. 
        Always call the blood bank directly using the phone numbers listed to verify real-time unit availability.
    </div>
    """, unsafe_allow_html=True)

    col_search, col_info = st.columns([1, 2])
    with col_search:
        selected_bg = st.selectbox(
            "Filter by Blood Group",
            ["All Groups", "A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
        )

    with col_info:
        st.info("💡 **Quick Medical Knowledge**: Group **O-** is the universal red blood cell donor, and **AB+** is the universal plasma recipient.")

    blood_df = db.get_blood_inventory(blood_group=selected_bg)

    if not blood_df.empty:
        st.dataframe(blood_df[["bank_name", "blood_group", "units_available", "city", "contact_number", "last_updated"]], use_container_width=True, hide_index=True)
    else:
        st.warning("No blood banks found with the selected group.")


# ==============================================================================
# 7. ℹ️ ABOUT & DISCLAIMERS
# ==============================================================================
elif menu_selection == "ℹ️ About & Disclaimers":
    st.markdown('<div class="main-header">ℹ️ About CareConnect</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Project Overview & Hackathon Submission Details</div>', unsafe_allow_html=True)

    st.markdown("""
    ### 🎯 Hackathon Objective
    **CareConnect** was developed for the **FIT-FEST 2026 Hackathon** at **Flora Institute of Technology, Pune**.
    
    Small clinics and general practices face immense administrative overload using fragmented physical notebooks and WhatsApp messages. 
    CareConnect provides a unified, zero-clutter coordination hub designed to:
    * Eliminate lost paper records and double-booked visits.
    * Provide quick emergency coordination and triage logging.
    * Provide a centralized directory for blood bank availability in the Pune region.

    ---

    ### 🛠️ Technology Stack
    * **Frontend & Dashboard**: [Streamlit](https://streamlit.io/) (Pure Python)
    * **Database**: SQLite3 (`careconnect.db`)
    * **Containerization**: Docker
    * **Cloud Hosting**: Google Cloud Run (Port 8080)

    ---

    ### 🛡️ Ethical & Clinical Boundaries
    * CareConnect is **NOT** a medical diagnostic system.
    * It does not suggest medicines, calculate dosages, or make triage clinical judgments.
    * All emergency logs and blood bank numbers are simulated for hackathon evaluation.
    """)
