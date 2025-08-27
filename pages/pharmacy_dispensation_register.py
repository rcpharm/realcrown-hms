import streamlit as st
import pandas as pd
from supabase import create_client
from datetime import datetime
import uuid

# Initialize Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# Fetch data
@st.cache_data
def fetch_prescriptions():
    return supabase.table("prescriptions").select("*").eq("status", "pending").execute().data

@st.cache_data
def fetch_medicines():
    return supabase.table("medicines").select("id, name, unit").execute().data

@st.cache_data
def fetch_staff():
    return supabase.table("staff").select("id, full_name").execute().data

@st.cache_data
def fetch_patients():
    return supabase.table("patients").select("id, full_name").execute().data

prescriptions = fetch_prescriptions()
medicines = fetch_medicines()
staff = fetch_staff()
patients = fetch_patients()

# Helper functions
def get_medicine_name(mid):
    return next((m["name"] for m in medicines if m["id"] == mid), "Unknown")

def get_patient_name(pid):
    return next((p["full_name"] for p in patients if p["id"] == pid), "Unknown")

# Title
st.title("💊 Pharmacy Dispensation Register")

# Display pending prescriptions
st.subheader("📋 Pending Prescriptions")
df = pd.DataFrame(prescriptions)
df["Medicine"] = df["medication_id"].apply(get_medicine_name)
df["Patient"] = df["patient_id"].apply(get_patient_name)
df["Instructions"] = df["instructions"]
df["Prescribed At"] = pd.to_datetime(df["prescribed_at"]).dt.strftime("%Y-%m-%d %H:%M")
st.dataframe(df[["id", "Patient", "Medicine", "Instructions", "Prescribed At"]])

# Dispensation form
st.subheader("🧾 Dispense Medication")
selected_id = st.selectbox("Select Prescription ID", df["id"])
selected_prescription = df[df["id"] == selected_id].iloc[0]

dispensed_by = st.selectbox("Dispensed By", staff, format_func=lambda x: x["full_name"])
quantity_dispensed = st.number_input("Quantity Dispensed", min_value=1)
confirmed = st.checkbox("Confirmed by Patient")

if st.button("Submit Dispensation"):
    dispensation = {
        "id": str(uuid.uuid4()),
        "prescription_id": selected_id,
        "dispensed_by": dispensed_by["id"],
        "quantity_dispensed": quantity_dispensed,
        "dispensed_at": datetime.now().isoformat(),
        "confirmed_by_patient": confirmed
    }
    response = supabase.table("dispensations").insert(dispensation).execute()

    # Update prescription status
    supabase.table("prescriptions").update({"status": "dispensed"}).eq("id", selected_id).execute()

    if response.status_code == 201:
        st.success("✅ Medication dispensed and inventory updated.")
    else:
        st.error("❌ Failed to record dispensation.")
