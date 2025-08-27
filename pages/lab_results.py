import streamlit as st
from datetime import datetime
from supabase import create_client
from dotenv import load_dotenv
import os

# --- Load environment variables ---
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("🧬 Log Lab Results")

# --- Get staff ID from query or session ---
staff_id = st.query_params.get("staff_id") or st.session_state.get("staff_id")
if not staff_id:
    st.warning("Staff ID missing. Please log in.")
    st.stop()

# --- Fetch pending lab requests ---
pending = supabase.table("lab_requests").select("*").eq("status", "pending").order("created_at", desc=True).execute()

if pending.status_code != 200 or not pending.data:
    st.info("✅ No pending lab requests.")
else:
    for request in pending.data:
        label = f"{request['test_type']} | Lab No: {request.get('lab_number', 'N/A')} | Patient ID: {request['patient_id']}"
        with st.expander(label):
            result_value = st.text_area("Result Value", key=f"result_{request['id']}")
            result_notes = st.text_area("Result Notes", key=f"notes_{request['id']}")
            submit = st.button("Submit Result", key=f"submit_{request['id']}")

            if submit:
                if not result_value.strip():
                    st.warning("Result value cannot be empty.")
                else:
                    # Insert result
                    result_response = supabase.table("lab_results").insert({
                        "lab_request_id": request["id"],
                        "result_value": result_value,
                        "result_notes": result_notes,
                        "logged_by": staff_id,
                        "timestamp": datetime.utcnow().isoformat()
                    }).execute()

                    # Update request status
                    update_response = supabase.table("lab_requests").update({
                        "status": "completed"
                    }).eq("id", request["id"]).execute()

                    if result_response.status_code == 201 and update_response.status_code == 200:
                        st.success("✅ Result logged and request marked as completed.")
                    else:
                        st.error("❌ Failed to log result. Please try again.")
