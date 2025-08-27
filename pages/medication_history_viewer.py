import streamlit as st
import pandas as pd
from supabase import create_client
from datetime import datetime

# Initialize Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# Fetch data
@st.cache_data
def fetch_dispensations():
    return supabase.table("dispensations").select("*").execute().data

@st.cache_data
def fetch_prescriptions():
    return supabase.table("prescriptions").select("*").execute().data

@st.cache_data
def fetch_medicines():
    return supabase.table("medicines").select("id, name, unit").execute().data

@st.cache_data
def fetch_staff():
    return supabase.table("staff").select("id, full_name").execute().data

@st.cache_data
def fetch_patients():
    return supabase.table("patients").select("id, full_name").execute().data

# Load data
dispensations = fetch_dispensations()
prescriptions = fetch_prescriptions()
medicines = fetch_medicines()
staff = fetch_staff()
patients = fetch_patients()

# Helper functions
def get_name(table, id):
    return next((item["full_name"] for item in table if item["id"] == id), "Unknown")

def get_med_name(mid):
    return next((m["name"] for m in medicines if m["id"] == mid), "Unknown")

def get_prescription(pid):
    return next((p for p in prescriptions if p["id"] == pid), None)

# UI
st.title("🧾 Patient Medication History Viewer")

selected_patient = st.selectbox("Select Patient", patients, format_func=lambda x: x["full_name"])
patient_id = selected_patient["id"]

# Filter dispensations for selected patient
patient_dispensations = [
    d for d in dispensations
    if get_prescription(d["prescription_id"]) and get_prescription(d["prescription_id"])["patient_id"] == patient_id
]

# Filter widgets
st.subheader("🔎 Filter History")

start_date = st.date_input("Start Date", value=datetime(2024, 1, 1))
end_date = st.date_input("End Date", value=datetime.today())

med_options = sorted(set(get_med_name(p["medication_id"]) for p in prescriptions if p["patient_id"] == patient_id))
selected_med = st.selectbox("Medication", ["All"] + med_options)

clinicians = sorted(set(
    get_name(staff, p["prescribed_by"]) for p in prescriptions
    if p["patient_id"] == patient_id and "prescribed_by" in p
))
selected_clinician = st.selectbox("Prescriber", ["All"] + clinicians)

# Apply filters
filtered = []
for d in patient_dispensations:
    presc = get_prescription(d["prescription_id"])
    if not presc:
        continue

    disp_date = datetime.fromisoformat(d["dispensed_at"]).date()
    if not (start_date <= disp_date <= end_date):
        continue

    med_name = get_med_name(presc["medication_id"])
    if selected_med != "All" and med_name != selected_med:
        continue

    prescriber_name = get_name(staff, presc.get("prescribed_by", ""))
    if selected_clinician != "All" and prescriber_name != selected_clinician:
        continue

    confirmed = d["confirmed_by_patient"]
    follow_up = "⚠️ Follow-up Needed" if not confirmed else ""

    filtered.append({
        "Date": disp_date.strftime("%Y-%m-%d"),
        "Medication": med_name,
        "Instructions": presc["instructions"],
        "Quantity": d["quantity_dispensed"],
        "Dispensed By": get_name(staff, d["dispensed_by"]),
        "Prescribed By": prescriber_name,
        "Confirmed": "✅" if confirmed else "❌",
        "Flag": follow_up
    })

# Display results
st.subheader("📋 Medication History")
if filtered:
    st.dataframe(pd.DataFrame(filtered))
else:
    st.warning("No records match the selected filters.")
