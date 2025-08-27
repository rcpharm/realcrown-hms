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
            invites = supabase.table("staff_invites").select("email").execute().data
            invited_emails = [i["email"] for i in invites]

            if email not in invited_emails:
                st.warning("⚠️ This email is not on the invite list.")
                st.stop()

            # Step 2: Check for existing staff record
            existing_staff = supabase.table("staff").select("id").eq("email", email).execute().data
            if existing_staff:
                st.warning("⚠️ This email is already registered in the staff table.")
                st.stop()

            # Step 3: Create Supabase Auth user
            auth_response = supabase.auth.sign_up({
                "email": email,
                "password": password
            })

            if auth_response and auth_response.user:
                uid = auth_response.user.id

                # Step 4: Insert into staff table
                staff_payload = {
                    "id": str(uuid.uuid4()),
                    "full_name": name,
                    "email": email,
                    "phone_number": phone,
                    "gender": gender,
                    "role": role,
                    "status": status,
                    "uid": uid
                }

                insert_response = supabase.table("staff").insert(staff_payload).execute()
                if insert_response and insert_response.data:
                    st.success(f"✅ {name} registered successfully as `{role}`.")
                    # Step 5: Remove invite
                    supabase.table("staff_invites").delete().eq("email", email).execute()
                else:
                    st.error("❌ Failed to insert staff profile.")
            else:
                st.error("❌ Supabase Auth registration failed.")
        except Exception as e:
            st.error(f"❌ Registration failed: {e}")
    else:
        st.warning("⚠️ Please fill in all required fields.")
