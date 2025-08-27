import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
import pandas as pd
import os

# --- Load environment variables ---
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("📋 Lab Register Dashboard")

# --- Get staff ID for access control ---
staff_id = st.query_params.get("staff_id") or st.session_state.get("staff_id")
if not staff_id:
    st.warning("Staff ID missing. Please log in.")
    st.stop()

# --- Filters ---
status_filter = st.selectbox("Filter by Status", ["all", "pending", "completed"])
test_type_filter = st.text_input("Filter by Test Type")

# --- Fetch lab requests ---
query = supabase.table("lab_requests").select("*").order("created_at", desc=True)
if status_filter != "all":
    query = query.eq("status", status_filter)
if test_type_filter:
    query = query.ilike("test_type", f"%{test_type_filter}%")
requests_response = query.execute()
requests_df = pd.DataFrame(requests_response.data) if requests_response.status_code == 200 else pd.DataFrame()

# --- Fetch lab results ---
results_response = supabase.table("lab_results").select("*").execute()
results_df = pd.DataFrame(results_response.data) if results_response.status_code == 200 else pd.DataFrame()

# --- Fetch patients ---
patients_response = supabase.table("patients").select("id, full_name").execute()
patients_df = pd.DataFrame(patients_response.data) if patients_response.status_code == 200 else pd.DataFrame()

# --- Fetch visits with staff_id ---
visits_response = supabase.table("visits").select("id, staff_id").execute()
visits_df = pd.DataFrame(visits_response.data) if visits_response.status_code == 200 else pd.DataFrame()

# --- Fetch staff names ---
staff_response = supabase.table("staff").select("id, full_name").execute()
staff_df = pd.DataFrame(staff_response.data) if staff_response.status_code == 200 else pd.DataFrame()

# --- Merge all data ---
merged_df = (
    requests_df
    .merge(results_df, left_on="id", right_on="lab_request_id", how="left", suffixes=("", "_result"))
    .merge(patients_df, left_on="patient_id", right_on="id", how="left", suffixes=("", "_patient"))
    .merge(visits_df, left_on="visit_id", right_on="id", how="left", suffixes=("", "_visit"))
    .merge(staff_df, left_on="staff_id", right_on="id", how="left", suffixes=("", "_staff"))
)

# --- Result preview ---
def preview(row):
    if row["status"] == "completed" and pd.notna(row.get("result_value")):
        return f"{row['result_value'][:30]}... by {row['logged_by']}"
    return "—"

merged_df["Result Preview"] = merged_df.apply(preview, axis=1)
merged_df["created_at"] = pd.to_datetime(merged_df["created_at"]).dt.strftime("%Y-%m-%d %H:%M")

# --- Display table ---
display_df = merged_df[[
    "test_type", "full_name", "visit_id", "full_name_staff", "status", "created_at", "Result Preview"
]].rename(columns={
    "test_type": "Test Type",
    "full_name": "Patient Name",
    "visit_id": "Visit ID",
    "full_name_staff": "Ordered By",
    "status": "Status",
    "created_at": "Requested At"
})

st.dataframe(display_df, use_container_width=True)

# --- Export ---
st.download_button("📥 Export CSV", data=display_df.to_csv(index=False), file_name="lab_register.csv", mime="text/csv")

# --- Detail view ---
selected = st.selectbox("View Details for Request ID", merged_df["id"])
if selected:
    record = merged_df[merged_df["id"] == selected].iloc[0]
    st.subheader(f"🔍 Details for Request {selected}")
    st.write({
        "Test Type": record["test_type"],
        "Patient Name": record.get("full_name", "—"),
        "Visit ID": record["visit_id"],
        "Ordered By": record.get("full_name_staff", "—"),
        "Status": record["status"],
        "Requested At": record["created_at"],
        "Result Value": record.get("result_value", "—"),
        "Result Notes": record.get("result_notes", "—"),
        "Logged By": record.get("logged_by", "—"),
        "Timestamp": record.get("timestamp", "—")
    })
    
# --- Printable Summary ---
st.markdown("---")
st.subheader("🖨️ Printable Summary")

def format_summary(record):
    return f"""
    ### 🧪 Lab Request Summary

    **Test Type:** {record['test_type']}  
    **Patient Name:** {record.get('full_name', '—')}  
    **Visit ID:** {record['visit_id']}  
    **Ordered By:** {record.get('full_name_staff', '—')}  
    **Requested At:** {record['created_at']}  
    **Status:** {record['status']}

    ### 📊 Result Details

    **Result Value:** {record.get('result_value', '—')}  
    **Result Notes:** {record.get('result_notes', '—')}  
    **Logged By:** {record.get('logged_by', '—')}  
    **Timestamp:** {record.get('timestamp', '—')}
    """

if selected:
    st.markdown(format_summary(record), unsafe_allow_html=True)
    
# --- Print Button ---
st.markdown("""
    <button onclick="window.print()" style="
        background-color:#4CAF50;
        color:white;
        padding:10px 20px;
        border:none;
        border-radius:5px;
        font-size:16px;
        cursor:pointer;
        margin-top:10px;
    ">🖨️ Print This Summary</button>
""", unsafe_allow_html=True)
