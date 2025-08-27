import streamlit as st
from supabase import create_client
from datetime import datetime, timedelta
import uuid

# Initialize Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# Fetch patients, staff, ANC visits
@st.cache_data
def fetch_patients():
    return supabase.table("patients").select("id, full_name").execute().data

@st.cache_data
def fetch_staff():
    return supabase.table("staff").select("id, full_name").execute().data

@st.cache_data
def fetch_anc_visits():
    return supabase.table("anc_visits").select("*").order("recorded_at", desc=True).execute().data

patients = fetch_patients()
staff = fetch_staff()
anc_visits = fetch_anc_visits()

# Helper to get latest ANC visit per patient
def get_latest_anc(patient_id):
    for v in anc_visits:
        if v["patient_id"] == patient_id:
            return v
    return None

# UI
st.title("📅 ANC Schedule Tracker")

selected_patient = st.selectbox("Select Patient", patients, format_func=lambda x: x["full_name"])
staff_member = st.selectbox("Scheduled By", staff, format_func=lambda x: x["full_name"])

latest_visit = get_latest_anc(selected_patient["id"])
if latest_visit:
    st.markdown(f"**Last ANC Visit:** {latest_visit['recorded_at'][:10]} — GA: {latest_visit['gestational_age']} weeks")

    # Risk logic
    risk_factors = latest_visit.get("risk_factors", "").lower()
    risk_level = "low"
    if "hypertension" in risk_factors or "bleeding" in risk_factors or "previous c-section" in risk_factors:
        risk_level = "high"
    elif "anemia" in risk_factors or "twins" in risk_factors:
        risk_level = "moderate"

    # Schedule logic
    next_visit = datetime.now().date() + timedelta(days=14 if risk_level == "low" else 7)

    st.markdown(f"**Risk Level:** `{risk_level.upper()}`")
    st.markdown(f"**Next Visit Date:** `{next_visit}`")

    if st.button("Schedule Next ANC Visit"):
        schedule = {
            "id": str(uuid.uuid4()),
            "patient_id": selected_patient["id"],
            "last_anc_visit_id": latest_visit["id"],
            "gestational_age": latest_visit["gestational_age"],
            "next_visit_date": next_visit.isoformat(),
            "risk_level": risk_level,
            "flagged": risk_level == "high",
            "scheduled_by": staff_member["id"],
            "scheduled_at": datetime.now().isoformat()
        }
        response = supabase.table("anc_schedule").insert(schedule).execute()
        if response.status_code == 201:
            st.success("✅ ANC follow-up scheduled successfully.")
        else:
            st.error("❌ Failed to schedule follow-up.")
else:
    st.info("No ANC visit found for this patient.")
