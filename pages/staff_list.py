import streamlit as st
from supabase_config import supabase

st.title("Staff Directory")

# Admin-only access
if "user" not in st.session_state or st.session_state["user"]["role"] != "admin":
    st.warning("Access denied. Only admins can view staff list.")
    st.stop()

# Fetch all staff records
response = supabase.table("staff").select("*").execute()

if response.data:
    for staff in response.data:
        st.markdown(f"**{staff['name']}** — {staff['role']}")
        st.write(f"📧 {staff['email']} | 📱 {staff['phone']}")
        st.divider()
else:
    st.info("No staff records found.")
