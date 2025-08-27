import streamlit as st
from datetime import datetime
from supabase import create_client
import os
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# --- Initialize Supabase client ---
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Context: visit_id, patient_id, staff_id ---
visit_id = st.query_params.get("visit_id")
patient_id = st.query_params.get("patient_id")
staff_id = st.query_params.get("staff_id")

st.title("🧪 Lab Test Request")

# --- Lab Test Options ---
lab_tests = [
    "Complete Blood Count (CBC)",
    "Malaria Rapid Test",
    "HIV Test",
    "Urinalysis",
    "Blood Sugar (Glucose)",
    "Liver Function Test (LFT)",
    "Kidney Function Test (KFT)",
    "Stool Analysis",
    "Pregnancy Test",
    "Tuberculosis (TB) Test",
    "COVID-19 PCR",
    "Hemoglobin",
    "Syphilis (RPR)",
    "Hepatitis B Surface Antigen",
    "Hepatitis C Antibody",
    "Electrolytes Panel",
    "Thyroid Function Test",
    "Prostate Specific Antigen (PSA)",
    "Pap Smear",
    "Blood Grouping"
    "Crossmatch"
]

# --- Lab Request Form ---
with st.form("lab_request_form"):
    selected_tests = st.multiselect("Select Lab Tests", lab_tests)
    priority = st.radio("Priority", ["Routine", "Urgent"])
    notes = st.text_area("Additional Notes", "")
    submit = st.form_submit_button("Submit Request")

# --- Submission Logic ---
if submit:
    if not selected_tests:
        st.warning("Please select at least one test.")
    elif not visit_id or not patient_id or not staff_id:
        st.error("Missing visit or patient context.")
    else:
        success_count = 0
        for test in selected_tests:
            response = supabase.table("lab_requests").insert({
                "visit_id": visit_id,
                "patient_id": patient_id,
                "requested_by": staff_id,
                "test_type": test,
                "priority": priority.lower(),
                "notes": notes,
                "status": "pending",
                "created_at": datetime.utcnow().isoformat()
            }).execute()

            if response.status_code == 201:
                success_count += 1

        if success_count:
            st.success(f"{success_count} lab request(s) submitted.")
            st.experimental_set_query_params(patient_id=patient_id)
            st.switch_page("lab_register.py")
        else:
            st.error("Failed to submit lab requests.")
