import streamlit as st
from supabase_config import supabase
from datetime import datetime

st.title("Register New Patient")

# 📋 Input fields
name = st.text_input("Full Name")
age = st.number_input("Age", min_value=0, max_value=120)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
contact = st.text_input("Contact Number")
next_of_kin = st.text_input("Next of Kin")

# 🏡 Village selection with add-new option
villages_data = supabase.table("villages").select("id", "name").execute().data
village_names = [v["name"] for v in villages_data]
village_choice = st.selectbox("Village", village_names + ["Add new..."])

if village_choice == "Add new...":
    new_village = st.text_input("Enter new village name")
    if new_village:
        insert_response = supabase.table("villages").insert({"name": new_village}).execute()
        if insert_response.status_code == 201:
            st.success(f"Village '{new_village}' added.")
            village_choice = new_village
            villages_data = supabase.table("villages").select("id", "name").execute().data
            village_names = [v["name"] for v in villages_data]

# 🏥 Entry Department
departments = [
    "OPD", "IPD", "ANC", "Emergency", "Maternity",
    "Imaging", "Pediatrics", "Surgery", "Dental", "Psychiatry", "Other"
]
entry_department = st.selectbox("Entry Department", departments)

if entry_department == "Other":
    custom_department = st.text_input("Specify other department")
    if custom_department:
        entry_department = custom_department

# 👤 Created by (select from staff table)
staff_data = supabase.table("staff").select("id", "full_name").execute().data
staff_names = {s["full_name"]: s["id"] for s in staff_data}
created_by_name = st.selectbox("Created by", list(staff_names.keys()))
created_by_id = staff_names[created_by_name]

# 🧾 Register button
if st.button("Register Patient"):
    if name and age and contact and next_of_kin and village_choice and entry_department:
        try:
            village_id = next((v["id"] for v in villages_data if v["name"] == village_choice), None)
            timestamp = datetime.now().isoformat()

            patient_data = {
                "full_name": name,
                "age": age,
                "gender": gender,
                "contact_number": contact,
                "next_of_kin": next_of_kin,
                "village_id": village_id,
                "entry_department": entry_department,
                "created_at": timestamp,
                "created_by": created_by_id
            }

            response = supabase.table("patients").insert(patient_data).execute()

            if response.status_code == 201:
                st.success(f"Patient '{name}' registered successfully.")
            else:
                st.error("Failed to register patient.")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please fill in all required fields.")
