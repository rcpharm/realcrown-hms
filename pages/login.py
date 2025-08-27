import streamlit as st
from supabase_config import supabase
import streamlit_authenticator as stauth  # Optional if you want a UI wrapper
import time

st.title("Staff Login")

# Input fields
email = st.text_input("Email")
password = st.text_input("Password", type="password")

# Login button
if st.button("Login"):
    if email and password:
        try:
            user = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            if user:
                st.success("Login successful!")
                st.write("Welcome,", user.user.email)

                # Fetch staff profile
                staff = supabase.table("staff").select("*").eq("uid", user.user.id).single().execute()
                if staff.data:
                    st.write("Role:", staff.data["role"])
                    st.session_state["user"] = staff.data
                    time.sleep(1)
                    st.switch_page("pages/dashboard.py")
                else:
                    st.warning("No staff profile found for this user.")
            else:
                st.error("Login failed. Please check your credentials.")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter both email and password.")
 
