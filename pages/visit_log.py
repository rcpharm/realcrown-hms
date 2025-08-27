import streamlit as st
from supabase_config import supabase
from datetime import datetime

st.title("🩺 Log Patient Visit")

# 👤 Select patient
patients = supabase.table("patients").select("id", "full_name").execute().data
patient_map = {p["full_name"]: p["id"] for p in patients}
selected_patient = st.selectbox("Select Patient", list(patient_map.keys()))
patient_id = patient_map[selected_patient]

# 👨‍⚕️ Select staff
staff = supabase.table("staff").select("id", "full_name").execute().data
staff_map = {s["full_name"]: s["id"] for s in staff}
selected_staff = st.selectbox("Attended By", list(staff_map.keys()))
staff_id = staff_map[selected_staff]

# 📝 Visit notes
notes = st.text_area("Visit Notes")
diagnosis = st.text_input("Diagnosis")
prescription = st.text_area("Prescription")
timestamp = datetime.now().isoformat()

if st.button("Log Visit"):
    # Step 1: Insert into visits
    visit = supabase.table("visits").insert({
        "patient_id": patient_id,
        "staff_id": staff_id,
        "notes": notes,
        "timestamp": timestamp
    }).execute()

    if visit.status_code == 201:
        visit_id = visit.data[0]["id"]

        # Step 2: Insert into visit_details
        details = supabase.table("visit_details").insert({
            "visit_id": visit_id,
            "diagnosis": diagnosis,
            "prescription": prescription,
            "recorded_by": staff_id
        }).execute()

        if details.status_code == 201:
            st.success("✅ Visit and clinical details logged successfully.")
        else:
            st.warning("Visit saved, but failed to log diagnosis/prescription.")
    else:

        st.error("❌ Failed to log visit.")
        
st.experimental_set_query_params(visit_id=new_visit_id)
st.switch_page("visit_details.py")
