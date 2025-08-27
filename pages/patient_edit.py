import streamlit as st
from supabase_config import supabase

st.title("Edit Patient Record")

# 🔍 Search by name
search_name = st.text_input("Search Patient by Name")
if search_name:
    results = supabase.table("patients").select("*").ilike("full_name", f"%{search_name}%").execute().data
    if results:
        selected = st.selectbox("Select Patient", [r["full_name"] for r in results])
        patient = next(p for p in results if p["full_name"] == selected)

        # 📝 Editable fields
        new_name = st.text_input("Full Name", value=patient["full_name"])
        new_age = st.number_input("Age", value=patient["age"], min_value=0)
        new_gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(patient["gender"]))
        new_contact = st.text_input("Contact Number", value=patient["contact_number"])
        new_next_of_kin = st.text_input("Next of Kin", value=patient["next_of_kin"])

        if st.button("Update Patient"):
            update = supabase.table("patients").update({
                "full_name": new_name,
                "age": new_age,
                "gender": new_gender,
                "contact_number": new_contact,
                "next_of_kin": new_next_of_kin
            }).eq("id", patient["id"]).execute()

            if update.status_code == 200:
                st.success("Patient updated successfully.")
            else:
                st.error("Update failed.")
    else:
        st.info("No matching patients found.")
