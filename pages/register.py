import streamlit as st
from supabase_config import supabase
import uuid
import requests

st.title("Staff Registration")

# 📋 Input fields
name = st.text_input("Full Name")
email = st.text_input("Email")
password = st.text_input("Password", type="password")
phone = st.text_input("Phone Number")
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
role = st.selectbox("Role", [
    "admin", "medical_officer", "clinical_officer", "receptionist",
    "nurse", "midwife", "lab_technician", "lab_assistant",
    "sonographer", "radiographer", "accountant"
])
status = st.checkbox("Active", value=True)
photo = st.file_uploader("Upload Profile Photo", type=["jpg", "jpeg", "png"])

# 🧾 Register button
if st.button("Register"):
    if name and email and password and role:
        try:
            # Step 1: Check invite list
            invites = supabase.table("staff_invites").select("email").execute().data
            invited_emails = [i["email"] for i in invites]

            if email not in invited_emails:
                st.warning("This email is not on the invite list.")
                st.stop()

            # Step 2: Create Supabase Auth user
            auth_response = supabase.auth.sign_up({
                "email": email,
                "password": password
            })

            if auth_response.user:
                uid = auth_response.user.id

                # Step 3: Upload profile photo
                photo_url = None
                if photo:
                    file_ext = photo.name.split(".")[-1]
                    file_name = f"{uuid.uuid4()}.{file_ext}"
                    file_bytes = photo.read()  # Convert UploadedFile to bytes
                    upload_response = supabase.storage.from_("staff_photos").upload(file_name, file_bytes)
                    if upload_response:
                        photo_url = supabase.storage.from_("staff_photos").get_public_url(file_name)

                # Step 4: Insert into staff table
                staff_response = supabase.table("staff").insert({
                    "full_name": name,
                    "email": email,
                    "phone_number": phone,
                    "gender": gender,
                    "role": role,
                    "status": status,
                    "uid": uid,
                    "photo_url": photo_url
                }).execute()

                if staff_response.status_code == 201:
                    st.success(f"{name} registered successfully as {role}!")

                    # Optional: Remove invite after use
                    supabase.table("staff_invites").delete().eq("email", email).execute()

                else:
                    st.error("Failed to insert staff profile.")
            else:
                st.error("Auth registration failed.")
        except Exception as e:
            st.error(f"Registration failed: {e}")
    else:
        st.warning("Please fill in all required fields.")

