import streamlit as st
from supabase_config import supabase
import uuid

st.title("🧑‍⚕️ Staff Registration")

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

# 🧾 Register button
if st.button("Register"):
    if name and email and password and role:
        try:
            # Step 1: Check invite list
            invites_response = supabase.table("staff_invites").select("email").execute()
            if invites_response.error:
                st.error(f"❌ Failed to fetch invite list: {invites_response.error.message}")
                st.stop()

            invited_emails = [i["email"] for i in invites_response.data]
            if email not in invited_emails:
                st.warning("⚠️ This email is not on the invite list.")
                st.stop()

            # Step 2: Create Supabase Auth user
            auth_response = supabase.auth.sign_up({
                "email": email,
                "password": password
            })

            if auth_response.user:
                uid = auth_response.user.id

                # Step 3: Insert into staff table
                insert_response = supabase.table("staff").insert({
                    "id": str(uuid.uuid4()),
                    "full_name": name,
                    "email": email,
                    "phone_number": phone,
                    "gender": gender,
                    "role": role,
                    "status": status,
                    "uid": uid
                }).execute()

                if insert_response.error is None:
                    st.success(f"✅ {name} registered successfully as `{role}`.")
                    # Step 4: Remove invite
                    supabase.table("staff_invites").delete().eq("email", email).execute()
                else:
                    st.error(f"❌ Failed to insert staff profile: {insert_response.error.message}")
            else:
                st.error("❌ Supabase Auth registration failed.")
        except Exception as e:
            st.error(f"❌ Registration failed: {e}")
    else:
        st.warning("⚠️ Please fill in all required fields.")
