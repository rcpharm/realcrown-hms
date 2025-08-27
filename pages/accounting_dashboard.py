import streamlit as st
import pandas as pd
from supabase import create_client
from datetime import datetime
import uuid

# Supabase init
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# Fetch data
@st.cache_data
def fetch_charges():
    return supabase.table("charges").select("*").execute().data

@st.cache_data
def fetch_payments():
    return supabase.table("payments").select("*").execute().data

@st.cache_data
def fetch_staff():
    return supabase.table("staff").select("id, full_name").execute().data

@st.cache_data
def fetch_patients():
    return supabase.table("patients").select("id, full_name").execute().data

charges = fetch_charges()
payments = fetch_payments()
staff = fetch_staff()
patients = fetch_patients()

# Helper
def get_name(table, id):
    return next((x["full_name"] for x in table if x["id"] == id), "Unknown")

def get_patient_name(pid):
    return get_name(patients, pid)

# UI
st.title("💰 Accounting Dashboard")

# Charges table
st.subheader("📋 Charges")
charges_df = pd.DataFrame(charges)
charges_df["Patient"] = charges_df["patient_id"].apply(get_patient_name)
charges_df["Charged By"] = charges_df["charged_by"].apply(lambda x: get_name(staff, x))
charges_df["Charged At"] = pd.to_datetime(charges_df["charged_at"]).dt.strftime("%Y-%m-%d %H:%M")
st.dataframe(charges_df[["Patient", "service", "amount", "Charged By", "Charged At"]])

# Payment form
st.subheader("🧾 Record Payment")
selected_charge = st.selectbox("Select Charge", charges, format_func=lambda c: f"{get_patient_name(c['patient_id'])} - {c['service']} ({c['amount']})")
amount_paid = st.number_input("Amount Paid", min_value=0.0, max_value=selected_charge["amount"])
method = st.selectbox("Payment Method", ["cash", "insurance", "waiver"])
staff_member = st.selectbox("Paid By", staff, format_func=lambda x: x["full_name"])

if st.button("Submit Payment"):
    payment = {
        "id": str(uuid.uuid4()),
        "charge_id": selected_charge["id"],
        "amount_paid": amount_paid,
        "payment_method": method,
        "paid_by": staff_member["id"],
        "paid_at": datetime.now().isoformat()
    }
    response = supabase.table("payments").insert(payment).execute()
    if response.status_code == 201:
        st.success("✅ Payment recorded successfully!")
    else:
        st.error("❌ Failed to record payment.")
