import streamlit as st
from supabase import create_client
from datetime import datetime
import uuid

# Supabase init
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# Fetch deliveries and staff
@st.cache_data
def fetch_deliveries():
    return supabase.table("deliveries").select("*").execute().data

@st.cache_data
def fetch_staff():
    return supabase.table("staff").select("id, full_name").execute().data

deliveries = fetch_deliveries()
staff = fetch_staff()

# UI
st.title("👶 Newborn Registration")

delivery = st.selectbox("Select Delivery", deliveries, format_func=lambda d: f"{d['delivery_date']} - {d['delivery_type']} ({d['baby_count']} baby{'ies' if d['baby_count'] > 1 else ''})")
baby_number = st.number_input("Baby Number", min_value=1, max_value=delivery["baby_count"])
sex = st.selectbox("Sex", ["male", "female", "unknown"])
birth_weight = st.number_input("Birth Weight (kg)", min_value=0.5, max_value=6.0)
apgar_score = st.text_input("Apgar Score", placeholder="e.g. 8/10")
complications = st.text_area("Complications (if any)")
staff_member = st.selectbox("Registered By", staff, format_func=lambda x: x["full_name"])

if st.button("Register Newborn"):
    newborn = {
        "id": str(uuid.uuid4()),
        "delivery_id": delivery["id"],
        "baby_number": baby_number,
        "sex": sex,
        "birth_weight": birth_weight,
        "apgar_score": apgar_score,
        "complications": complications,
        "registered_by": staff_member["id"],
        "registered_at": datetime.now().isoformat()
    }
    response = supabase.table("newborns").insert(newborn).execute()
    if response.status_code == 201:
        st.success("✅ Newborn registered successfully!")
    else:
        st.error("❌ Failed to register newborn.")
