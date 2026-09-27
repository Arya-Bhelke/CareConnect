# 🏥 CareConnect
### Clinic Appointment & Emergency Coordination System
**FIT-FEST 2026 Hackathon | Flora Institute of Technology, Pune**

CareConnect is a streamlined, lightweight administrative and emergency coordination web application designed for small clinics, general practitioners, and citizens. It replaces manual paper notebooks and unorganized phone bookings with structured digital workflows, while providing rapid coordination for emergency ambulance requests and local blood bank availability.

---

## ⚠️ Important Ethical & Medical Disclaimer
> **CareConnect is strictly an administrative and emergency coordination platform.**  
> It does **NOT** provide medical diagnoses, treatment recommendations, clinical decisions, or triage advice. Emergency requests and blood bank stocks shown in demonstrations are simulated for hackathon evaluation. In actual emergencies, citizens must dial national helplines **108** (Ambulance) or **112** (National Emergency).

---

## 🌟 Key Features

1. **Dashboard & Live Analytics**:
   - Real-time metrics tracking total registered patients, today's appointments, active emergencies, and total blood units.
2. **Patient Registration**:
   - Quick digital intake capturing full name, age, gender, contact number, blood group, and city.
3. **Appointment Booking & Management**:
   - Schedule visits with doctors across departments.
   - Live status toggles: *Scheduled*, *Completed*, *Cancelled*.
4. **Emergency & Ambulance Coordination**:
   - Log urgent coordination requests with caller details, pickup location, and triage urgency (*Critical*, *Moderate*, *Non-Critical*).
   - Instant display of local emergency helplines (108 / 112).
5. **Blood Bank Directory**:
   - Search Pune blood banks by blood group (A+, B+, O+, AB+, etc.).
   - Displays real-time stock units and direct hospital contact numbers.

---

## 🛠️ Technology Stack

- **Frontend & UI**: [Streamlit](https://streamlit.io/) (Pure Python)
- **Backend & Logic**: Python 3 standard library
- **Database**: SQLite3 (`careconnect.db`)
- **Containerization**: Docker
- **Deployment Platform**: Google Cloud Run (Port 8080)

---

## 🚀 How to Run Locally

### 1. Prerequisites
Ensure you have Python 3.9+ installed on your system.

### 2. Install Dependencies
Open your terminal inside the `CareConnect` folder and run:
```bash
pip install -r requirements.txt
```

### 3. Launch the Application
Run the Streamlit app:
```bash
streamlit run app.py
```
The application will open automatically in your browser at `http://localhost:8501`.

---

## 🐳 Running with Docker
```bash
# Build the Docker container image
docker build -t careconnect .

# Run container on port 8080
docker run -p 8080:8080 careconnect
```
Visit `http://localhost:8080` in your browser.

---

## ☁️ Deployment to Google Cloud Run
```bash
# Authenticate with Google Cloud
gcloud auth login

# Set active Google Cloud project
gcloud config set project YOUR_PROJECT_ID

# Deploy directly from source
gcloud run deploy careconnect \
  --source . \
  --region asia-south1 \
  --platform managed \
  --allow-unauthenticated
```
