import streamlit as st
from supabase import create_client
from datetime import datetime
import uuid

# Initialize Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# Fetch patients, visits, staff
@st.cache_data
def fetch_patients():
    return supabase.table("patients").select("id, full_name").execute().data

@st.cache_data
def fetch_visits():
    return supabase.table("visits").select("id, patient_id").execute().data

@st.cache_data
def fetch_staff():
    return supabase.table("staff").select("id, full_name").execute().data

patients = fetch_patients()
visits = fetch_visits()
staff = fetch_staff()

# Helper to show patient name from visit
def get_patient_name(visit_id):
    visit = next((v for v in visits if v["id"] == visit_id), None)
    if visit:
        patient = next((p for p in patients if p["id"] == visit["patient_id"]), None)
        return patient["full_name"] if patient else "Unknown"
    return "Unknown"

# UI
st.title("🤰 ANC Visit Logger")

with st.form("anc_form"):
    visit = st.selectbox("Select Visit", visits, format_func=lambda v: f"{get_patient_name(v['id'])]} ({v['id'][:8]})")
    staff_member = st.selectbox("Recorded By", staff, format_func=lambda x: x["full_name"])
    gest_age = st.number_input("Gestational Age (weeks)", min_value=4, max_value=42)
    bp = st.text_input("Blood Pressure", placeholder="e.g. 120/80")
    weight = st.number_input("Weight (kg)", min_value=30.0, max_value=150.0)
    fetal_heartbeat = st.checkbox("Fetal Heartbeat Heard")
    risk_factors = st.text_area("Risk Factors", placeholder="e.g. hypertension, previous C-section")
    notes = st.text_area("Additional Notes")
    submitted = st.form_submit_button("Submit ANC Visit")

    if submitted:
        visit_data = {
            "id": str(uuid.uuid4()),
            "patient_id": visit["patient_id"],
            "visit_id": visit["id"],
            "gestational_age": gest_age,
            "blood_pressure": bp,
            "weight_kg": weight,
            "fetal_heartbeat": fetal_heartbeat,
            "risk_factors": risk_factors,
            "notes": notes,
            "recorded_by": staff_member["id"],
            "recorded_at": datetime.now().isoformat()
        }
        response = supabase.table("anc_visits").insert(visit_data).execute()
        if response.status_code == 201:
            st.success("✅ ANC visit recorded successfully!")
        else:
            st.error("❌ Failed to record ANC visit.")
