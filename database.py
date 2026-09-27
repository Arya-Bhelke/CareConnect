"""
database.py - Database management module for CareConnect
Handles SQLite database creation, schema setup, sample data seeding, and CRUD queries.
"""

import sqlite3
import os
from datetime import datetime, date
import pandas as pd

# Path to the SQLite database file
DB_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "careconnect.db")


def get_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn


def init_db():
    """Initialize the database schema and seed initial sample data if empty."""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Patients Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT,
        blood_group TEXT NOT NULL,
        city TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 2. Appointments Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        doctor_name TEXT NOT NULL,
        department TEXT NOT NULL,
        appointment_date TEXT NOT NULL,
        appointment_time TEXT NOT NULL,
        reason TEXT,
        status TEXT DEFAULT 'Scheduled',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (patient_id) REFERENCES patients (id)
    )
    """)

    # 3. Emergency Requests Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emergency_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        caller_name TEXT NOT NULL,
        contact_number TEXT NOT NULL,
        pickup_address TEXT NOT NULL,
        urgency_level TEXT NOT NULL,
        notes TEXT,
        status TEXT DEFAULT 'Pending',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 4. Blood Inventory Table (Simulated Pune Blood Banks)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS blood_inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        blood_group TEXT NOT NULL,
        bank_name TEXT NOT NULL,
        city TEXT NOT NULL,
        units_available INTEGER NOT NULL,
        contact_number TEXT NOT NULL,
        last_updated TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()

    # Seed initial demo data if tables are empty
    seed_initial_data(conn)
    conn.close()


def seed_initial_data(conn):
    """Seed initial sample data for demonstration during hackathon presentation."""
    cursor = conn.cursor()

    # Seed Blood Inventory if empty
    cursor.execute("SELECT COUNT(*) FROM blood_inventory")
    if cursor.fetchone()[0] == 0:
        sample_blood_data = [
            ("A+", "Sassoon General Hospital Blood Bank", "Pune", 18, "+91 20 2612 8000"),
            ("A-", "Sassoon General Hospital Blood Bank", "Pune", 6, "+91 20 2612 8000"),
            ("B+", "Ruby Hall Clinic Blood Bank", "Pune", 24, "+91 20 6645 5100"),
            ("B-", "Ruby Hall Clinic Blood Bank", "Pune", 5, "+91 20 6645 5100"),
            ("O+", "Sahyadri Super Speciality Hospital", "Pune", 30, "+91 20 6721 3000"),
            ("O-", "Sahyadri Super Speciality Hospital", "Pune", 8, "+91 20 6721 3000"),
            ("AB+", "Deenanath Mangeshkar Hospital Blood Bank", "Pune", 14, "+91 20 4015 1000"),
            ("AB-", "Deenanath Mangeshkar Hospital Blood Bank", "Pune", 4, "+91 20 4015 1000"),
            ("O+", "Poona Hospital & Research Centre", "Pune", 20, "+91 20 2433 1707"),
            ("B+", "Jehangir Hospital Blood Bank", "Pune", 16, "+91 20 6681 9999"),
            ("A+", "KEM Hospital Blood Bank", "Pune", 12, "+91 20 2606 4800"),
        ]
        cursor.executemany("""
        INSERT INTO blood_inventory (blood_group, bank_name, city, units_available, contact_number)
        VALUES (?, ?, ?, ?, ?)
        """, sample_blood_data)

    # Seed Sample Patients if empty
    cursor.execute("SELECT COUNT(*) FROM patients")
    if cursor.fetchone()[0] == 0:
        sample_patients = [
            ("Aarav Patil", 32, "Male", "9823012345", "aarav.patil@example.com", "O+", "Pune"),
            ("Sneha Deshmukh", 28, "Female", "9823054321", "sneha.d@example.com", "B+", "Pune"),
            ("Ramesh Joshi", 58, "Male", "9823098765", "ramesh.j@example.com", "A+", "Pune"),
        ]
        cursor.executemany("""
        INSERT INTO patients (full_name, age, gender, phone, email, blood_group, city)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, sample_patients)

    # Seed Sample Appointments if empty
    cursor.execute("SELECT COUNT(*) FROM appointments")
    if cursor.fetchone()[0] == 0:
        today_str = date.today().isoformat()
        sample_appointments = [
            (1, "Dr. Sunita Kulkarni", "General Medicine", today_str, "10:30 AM", "Routine health checkup", "Scheduled"),
            (2, "Dr. Anand Mehta", "Cardiology", today_str, "11:15 AM", "Chest tightness follow-up", "Scheduled"),
            (3, "Dr. Rajesh Shinde", "Orthopedics", today_str, "02:00 PM", "Knee joint stiffness", "Completed"),
        ]
        cursor.executemany("""
        INSERT INTO appointments (patient_id, doctor_name, department, appointment_date, appointment_time, reason, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, sample_appointments)

    # Seed Sample Emergency Request if empty
    cursor.execute("SELECT COUNT(*) FROM emergency_requests")
    if cursor.fetchone()[0] == 0:
        sample_emergencies = [
            ("Vikram Rao", "9890112233", "Flat 402, Shivajinagar, Pune", "Moderate", "Elderly patient feeling dizzy with shortness of breath", "Pending"),
        ]
        cursor.executemany("""
        INSERT INTO emergency_requests (caller_name, contact_number, pickup_address, urgency_level, notes, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """, sample_emergencies)

    conn.commit()


# ==============================================================================
# PATIENT FUNCTIONS
# ==============================================================================

def add_patient(full_name, age, gender, phone, email, blood_group, city):
    """Add a new patient record and return the generated patient ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO patients (full_name, age, gender, phone, email, blood_group, city)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (full_name.strip(), age, gender, phone.strip(), email.strip(), blood_group, city.strip()))
    patient_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return patient_id


def get_all_patients():
    """Retrieve all patients as a pandas DataFrame."""
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM patients ORDER BY id DESC", conn)
    conn.close()
    return df


def get_patient_dropdown_options():
    """Return a list of (id, display_label) tuples for selection dropdowns."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name, phone, blood_group FROM patients ORDER BY full_name ASC")
    rows = cursor.fetchall()
    conn.close()
    options = {}
    for r in rows:
        label = f"ID #{r['id']} - {r['full_name']} ({r['phone']}) [{r['blood_group']}]"
        options[label] = r['id']
    return options


# ==============================================================================
# APPOINTMENT FUNCTIONS
# ==============================================================================

def add_appointment(patient_id, doctor_name, department, appointment_date, appointment_time, reason):
    """Book a new appointment."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO appointments (patient_id, doctor_name, department, appointment_date, appointment_time, reason, status)
    VALUES (?, ?, ?, ?, ?, ?, 'Scheduled')
    """, (patient_id, doctor_name, department, appointment_date, appointment_time, reason.strip()))
    appointment_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return appointment_id


def get_all_appointments(filter_status=None, filter_date=None):
    """Retrieve appointments joined with patient details."""
    conn = get_connection()
    query = """
    SELECT 
        a.id AS appointment_id,
        p.full_name AS patient_name,
        p.phone AS patient_phone,
        p.blood_group,
        a.doctor_name,
        a.department,
        a.appointment_date,
        a.appointment_time,
        a.reason,
        a.status
    FROM appointments a
    JOIN patients p ON a.patient_id = p.id
    WHERE 1=1
    """
    params = []
    if filter_status and filter_status != "All":
        query += " AND a.status = ?"
        params.append(filter_status)
    if filter_date:
        query += " AND a.appointment_date = ?"
        params.append(filter_date)

    query += " ORDER BY a.appointment_date ASC, a.appointment_time ASC"
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df


def update_appointment_status(appointment_id, new_status):
    """Update the status of an appointment (Scheduled / Completed / Cancelled)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE appointments 
    SET status = ? 
    WHERE id = ?
    """, (new_status, appointment_id))
    conn.commit()
    conn.close()


# ==============================================================================
# EMERGENCY & AMBULANCE FUNCTIONS
# ==============================================================================

def add_emergency_request(caller_name, contact_number, pickup_address, urgency_level, notes):
    """Log a simulated emergency or ambulance coordination request."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO emergency_requests (caller_name, contact_number, pickup_address, urgency_level, notes, status)
    VALUES (?, ?, ?, ?, ?, 'Pending')
    """, (caller_name.strip(), contact_number.strip(), pickup_address.strip(), urgency_level, notes.strip()))
    req_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return req_id


def get_all_emergency_requests():
    """Retrieve all emergency coordination logs."""
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM emergency_requests ORDER BY id DESC", conn)
    conn.close()
    return df


def update_emergency_status(request_id, new_status):
    """Update emergency request status (Pending / Dispatched / Resolved)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE emergency_requests 
    SET status = ? 
    WHERE id = ?
    """, (new_status, request_id))
    conn.commit()
    conn.close()


# ==============================================================================
# BLOOD INVENTORY FUNCTIONS
# ==============================================================================

def get_blood_inventory(blood_group=None):
    """Retrieve blood bank availability. Optional filter by blood group."""
    conn = get_connection()
    if blood_group and blood_group != "All Groups":
        df = pd.read_sql_query(
            "SELECT * FROM blood_inventory WHERE blood_group = ? ORDER BY units_available DESC",
            conn,
            params=[blood_group]
        )
    else:
        df = pd.read_sql_query(
            "SELECT * FROM blood_inventory ORDER BY blood_group ASC, units_available DESC",
            conn
        )
    conn.close()
    return df


# ==============================================================================
# DASHBOARD METRICS
# ==============================================================================

def get_dashboard_metrics():
    """Calculate real-time count metrics for the dashboard."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM patients")
    total_patients = cursor.fetchone()[0]

    today_str = date.today().isoformat()
    cursor.execute("SELECT COUNT(*) FROM appointments WHERE appointment_date = ?", (today_str,))
    today_appointments = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM appointments WHERE status = 'Scheduled'")
    pending_appointments = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM emergency_requests WHERE status = 'Pending'")
    active_emergencies = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(units_available) FROM blood_inventory")
    total_blood_units = cursor.fetchone()[0] or 0

    conn.close()

    return {
        "total_patients": total_patients,
        "today_appointments": today_appointments,
        "pending_appointments": pending_appointments,
        "active_emergencies": active_emergencies,
        "total_blood_units": total_blood_units
    }


if __name__ == "__main__":
    print("Initializing CareConnect SQLite database...")
    init_db()
    print("Database initialized successfully!")
    metrics = get_dashboard_metrics()
    print("Initial metrics:", metrics)
