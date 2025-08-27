import streamlit as st
from supabase import create_client
from datetime import datetime
import uuid

# Initialize Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# Fetch patients and staff
@st.cache_data
def fetch_patients():
    return supabase.table("patients").select("id, full_name").execute().data

@st.cache_data
def fetch_staff():
    return supabase.table("staff").select("id, full_name").execute().data

patients = fetch_patients()
staff = fetch_staff()

# Imaging types (can be replaced with a dynamic fetch from imaging_types table)
imaging_options = ["X-ray", "Ultrasound", "CT", "MRI", "Echocardiogram"]

# Page title
st.title("📝 Submit Imaging Request")

# Form
with st.form("imaging_request_form"):
    patient = st.selectbox("Select Patient", patients, format_func=lambda x: x["full_name"])
    clinician = st.selectbox("Requested By", staff, format_func=lambda x: x["full_name"])
    imaging_type = st.selectbox("Imaging Type", imaging_options)
    clinical_notes = st.text_area("Clinical Notes / Reason for Request")
    submitted = st.form_submit_button("Submit Request")

    if submitted:
        new_request = {
            "id": str(uuid.uuid4()),
            "patient_id": patient["id"],
            "requested_by": clinician["id"],
            "imaging_type": imaging_type,
            "clinical_notes": clinical_notes,
            "request_date": datetime.now().isoformat(),
            "status": "pending"
        }
        response = supabase.table("imaging_requests").insert(new_request).execute()
        if response.status_code == 201:
            st.success("✅ Imaging request submitted successfully!")
        else:
            st.error("❌ Failed to submit request. Please try again.")
