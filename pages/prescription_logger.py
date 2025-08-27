import streamlit as st
from supabase import create_client
from datetime import datetime
import uuid

# Initialize Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# Fetch patients, visits, staff, and medicines
@st.cache_data
def fetch_patients():
    return supabase.table("patients").select("id, full_name").execute().data

@st.cache_data
def fetch_visits():
    return supabase.table("visits").select("id, patient_id").execute().data

@st.cache_data
def fetch_staff():
    return supabase.table("staff").select("id, full_name").execute().data

@st.cache_data
def fetch_medicines():
    return supabase.table("medicines").select("id, name, unit").execute().data

patients = fetch_patients()
visits = fetch_visits()
staff = fetch_staff()
medicines = fetch_medicines()

# Helper to show patient name from visit
def get_patient_name(visit_id):
    visit = next((v for v in visits if v["id"] == visit_id), None)
    if visit:
        patient = next((p for p in patients if p["id"] == visit["patient_id"]), None)
        return patient["full_name"] if patient else "Unknown"
    return "Unknown"

# Page title
st.title("💊 Prescription Logger")

# Form
with st.form("prescription_form"):
    visit = st.selectbox("Visit", visits, format_func=lambda v: f"{get_patient_name(v['id'])]} ({v['id'][:8]})")
    clinician = st.selectbox("Prescribed By", staff, format_func=lambda x: x["full_name"])
    medicine = st.selectbox("Medicine", medicines, format_func=lambda m: f"{m['name']} ({m['unit']})")
    dosage = st.text_input("Dosage Instructions", placeholder="e.g. 1 tablet twice daily")
    duration = st.text_input("Duration", placeholder="e.g. 5 days")
    notes = st.text_area("Additional Notes (optional)")
    submitted = st.form_submit_button("Submit Prescription")

    if submitted:
        prescription = {
            "id": str(uuid.uuid4()),
            "visit_id": visit["id"],
            "medication_id": medicine["id"],
            "medication_text": medicine["name"],
            "instructions": f"{dosage}, for {duration}",
            "notes": notes,
            "prescribed_by": clinician["id"],
            "prescribed_at": datetime.now().isoformat(),
            "status": "pending"
        }
        response = supabase.table("prescriptions").insert(prescription).execute()
        if response.status_code == 201:
            st.success("✅ Prescription submitted successfully!")
        else:
            st.error("❌ Failed to submit prescription.")
