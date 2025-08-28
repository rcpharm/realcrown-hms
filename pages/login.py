import streamlit as st
from supabase_config import supabase
import time

st.set_page_config(page_title="Staff Login", layout="centered")
st.title("🔐 Staff Login")

# 📋 Input fields
email = st.text_input("Email")
password = st.text_input("Password", type="password")

# 🔘 Login button
if st.button("Login"):
    if email and password:
        try:
            # 🔐 Step 1: Authenticate with Supabase
            user = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            if user and user.user:
                st.success("✅ Login successful!")
                st.write("Welcome,", user.user.email)

                # 📄 Step 2: Fetch staff profile
                staff = supabase.table("staff").select("*").eq("uid", user.user.id).single().execute()
                if staff.data:
                    profile = staff.data

                    # 🧠 Step 3: Store user info in session state
                    st.session_state["user"] = {
                        "name": profile.get("full_name", "Unknown"),
                        "role": profile.get("role", "guest"),
                        "uid": profile.get("uid"),
                        "email": profile.get("email"),
                        "id": profile.get("id")  # ✅ This is the staff_id
                    }
                    st.session_state["staff_id"] = profile.get("id")  # ✅ Explicit for modules that need it

                    time.sleep(1)
                    st.switch_page("pages/dashboard.py")
                else:
                    st.warning("⚠️ No staff profile found for this user.")
            else:
                st.error("❌ Login failed. Please check your credentials.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
    else:
        st.warning("⚠️ Please enter both email and password.")
