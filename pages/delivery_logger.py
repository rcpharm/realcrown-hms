import streamlit as st
from supabase import create_client
from datetime import datetime, date
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
st.title("👶 Maternity Delivery Logger")

with st.form("delivery_form"):
    visit = st.selectbox(
        "Select Visit",
        visits,
        format_func=lambda v: f"{get_patient_name(v['id'])} ({v['id'][:8]})"
    )
    staff_member = st.selectbox("Delivered By", staff, format_func=lambda x: x["full_name"])
    delivery_date = st.date_input("Delivery Date", value=date.today())
    delivery_type = st.selectbox("Delivery Type", ["normal", "c-section", "assisted"])
    outcome = st.selectbox("Outcome", ["live birth", "stillbirth", "multiple"])
    baby_count = st.number_input("Number of Babies", min_value=1, max_value=5, value=1)
    complications = st.text_area("Complications", placeholder="e.g. postpartum hemorrhage")
    notes = st.text_area("Additional Notes")
    submitted = st.form_submit_button("Log Delivery")

    if submitted:
        delivery = {
            "id": str(uuid.uuid4()),
            "patient_id": visit["patient_id"],
            "visit_id": visit["id"],
            "delivery_date": delivery_date.isoformat(),
            "delivery_type": delivery_type,
            "outcome": outcome,
            "baby_count": baby_count,
            "complications": complications,
            "notes": notes,
            "delivered_by": staff_member["id"],
            "recorded_at": datetime.now().isoformat()
        }
        response = supabase.table("deliveries").insert(delivery).execute()
        if response.status_code == 201:
            st.success("✅ Delivery logged successfully!")
        else:
            st.error("❌ Failed to log delivery.")
