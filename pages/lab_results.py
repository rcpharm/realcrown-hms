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

st.set_page_config(page_title="Log Lab Results", layout="wide")
st.title("🧬 Log Lab Results")

# --- Optional: derive staff ID from session if available ---
staff_id = (st.session_state.get("user") or {}).get("id") or None

# --- Fetch pending lab requests ---
pending_response = supabase.table("lab_requests").select("*").eq("status", "pending").order("created_at", desc=True).execute()
pending_data = pending_response.data or []

if not pending_data:
    st.info("✅ No pending lab requests.")
else:
    for request in pending_data:
        label = f"{request['test_type']} | Lab No: {request.get('lab_number', 'N/A')} | Patient ID: {request['patient_id']}"
        with st.expander(label):
            result_value = st.text_area("Result Value", key=f"result_{request['id']}")
            result_notes = st.text_area("Result Notes", key=f"notes_{request['id']}")
            submit = st.button("Submit Result", key=f"submit_{request['id']}")

            if submit:
                if not result_value.strip():
                    st.warning("⚠️ Result value cannot be empty.")
                else:
                    # Insert result
                    result_payload = {
                        "lab_request_id": request["id"],
                        "result_value": result_value,
                        "result_notes": result_notes,
                        "logged_by": staff_id,  # Optional attribution
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    result_response = supabase.table("lab_results").insert(result_payload).execute()

                    # Update request status
                    update_response = supabase.table("lab_requests").update({
                        "status": "completed"
                    }).eq("id", request["id"]).execute()

                    if result_response.data and update_response.data:
                        st.success("✅ Result logged and request marked as completed.")
                    else:
                        st.error("❌ Failed to log result. Please try again.")
