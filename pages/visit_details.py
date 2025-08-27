import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Get visit_id from query params or session
visit_id = st.query_params.get("visit_id") or st.session_state.get("visit_id")
if not visit_id:
    st.error("No visit ID found. Please log a visit first.")
    st.stop()

# Load visit info
visit = supabase.table("visits").select("*").eq("id", visit_id).single().execute().data
st.subheader(f"Visit Details for {visit['patient_name']} on {visit['visit_date']}")

# Diagnosis picker
diagnoses = supabase.table("diagnoses").select("id", "name").execute().data
diagnosis_map = {d["name"]: d["id"] for d in diagnoses}
selected_diagnosis = st.selectbox("Diagnosis", list(diagnosis_map.keys()))
diagnosis_id = diagnosis_map[selected_diagnosis]

# Medication picker
medications = supabase.table("medications").select("id", "name", "dosage", "form").execute().data
med_map = {
    f"{m['name']} ({m['dosage']} {m['form']})": m["id"]
    for m in medications
}
selected_meds = st.multiselect("Prescribed Medications", list(med_map.keys()))

# Notes
notes = st.text_area("Clinical Notes")

# Staff ID (assumed stored in session)
staff_id = st.session_state.get("staff_id")
if not staff_id:
    st.warning("Staff ID missing. Please log in.")
    st.stop()

# Submit
if st.button("Save Visit Details"):
    visit_detail = supabase.table("visit_details").insert({
        "visit_id": visit_id,
        "diagnosis_id": diagnosis_id,
        "notes": notes,
        "recorded_by": staff_id
    }).execute().data[0]

    for med_label in selected_meds:
        supabase.table("prescriptions").insert({
            "visit_detail_id": visit_detail["id"],
            "medication_id": med_map[med_label],
            "instructions": "As directed",
            "quantity": "1 pack"
        }).execute()

    st.success("Visit details saved successfully.")
