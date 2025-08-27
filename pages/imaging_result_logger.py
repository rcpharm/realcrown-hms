import streamlit as st
from supabase import create_client
from datetime import datetime
import uuid

# Initialize Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# Fetch pending imaging requests
@st.cache_data
def fetch_pending_requests():
    return supabase.table("imaging_requests").select("id, imaging_type, patient_id").eq("status", "pending").execute().data

# Fetch staff for attribution
@st.cache_data
def fetch_staff():
    return supabase.table("staff").select("id, full_name").execute().data

# Fetch patients for display
@st.cache_data
def fetch_patients():
    return supabase.table("patients").select("id, full_name").execute().data

requests = fetch_pending_requests()
staff = fetch_staff()
patients = fetch_patients()

# Helper to show patient name
def get_patient_name(patient_id):
    match = next((p["full_name"] for p in patients if p["id"] == patient_id), "Unknown")
    return match

# Page title
st.title("🧠 Imaging Result Logger")

# Form
with st.form("result_logger_form"):
    selected_request = st.selectbox(
        "Select Imaging Request",
        requests,
        format_func=lambda r: f"{r['imaging_type']} for {get_patient_name(r['patient_id'])]}"
    )
    reporter = st.selectbox("Reported By", staff, format_func=lambda x: x["full_name"])
    findings = st.text_area("Findings")
    impression = st.text_area("Impression / Interpretation")
    reviewed = st.checkbox("Mark as Reviewed")
    submitted = st.form_submit_button("Submit Report")

    if submitted:
        new_result = {
            "id": str(uuid.uuid4()),
            "request_id": selected_request["id"],
            "findings": findings,
            "impression": impression,
            "reported_by": reporter["id"],
            "report_date": datetime.now().isoformat(),
            "reviewed": reviewed
        }
        response = supabase.table("imaging_results").insert(new_result).execute()

        # Update request status to completed
        supabase.table("imaging_requests").update({"status": "completed"}).eq("id", selected_request["id"]).execute()

        if response.status_code == 201:
            st.success("✅ Imaging report submitted and request marked as completed!")
        else:
            st.error("❌ Failed to submit report. Please try again.")
