import streamlit as st
import pandas as pd
from supabase import create_client
from io import StringIO

# Initialize Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# Fetch imaging register data
@st.cache_data
def fetch_imaging_register():
    response = supabase.table("imaging_register_dashboard").select("*").execute()
    return response.data

# Load data
data = fetch_imaging_register()

# Title
st.title("📸 Imaging Register Dashboard")

# Sidebar filters
with st.sidebar:
    st.subheader("🔎 Filter Imaging Records")
    imaging_types = sorted(set(d["imaging_type"] for d in data))
    imaging_type = st.selectbox("Imaging Type", imaging_types)
    status = st.selectbox("Status", ["pending", "completed", "cancelled"])
    reviewed = st.selectbox("Reviewed", ["All", "Reviewed", "Not Reviewed"])

# Apply filters
filtered = [
    d for d in data
    if d["imaging_type"] == imaging_type
    and d["status"] == status
    and (reviewed == "All" or d["reviewed"] == (reviewed == "Reviewed"))
]

# Display table
df = pd.DataFrame(filtered)
st.dataframe(df[[
    "request_id", "patient_name", "requested_by", "imaging_type",
    "request_date", "status", "report_date", "reported_by",
    "findings", "impression", "reviewed"
]])

# Detail modal
selected = st.selectbox("🧾 View Imaging Report", [d["request_id"] for d in filtered])
record = next((d for d in filtered if d["request_id"] == selected), None)

if record:
    st.markdown(f"### 🧠 Imaging Report for {record['patient_name']}")
    st.write(f"**Requested by:** {record['requested_by']}")
    st.write(f"**Imaging Type:** {record['imaging_type']}")
    st.write(f"**Clinical Notes:** {record['clinical_notes']}")
    st.write(f"**Findings:** {record['findings']}")
    st.write(f"**Impression:** {record['impression']}")
    st.write(f"**Reported by:** {record['reported_by']}")
    st.write(f"**Reviewed:** {'✅' if record['reviewed'] else '❌'}")

    # Printable summary
    summary = f"""
    Imaging Report Summary
    -----------------------
    Patient: {record['patient_name']}
    Requested by: {record['requested_by']}
    Imaging Type: {record['imaging_type']}
    Clinical Notes: {record['clinical_notes']}
    Findings: {record['findings']}
    Impression: {record['impression']}
    Reported by: {record['reported_by']}
    Reviewed: {'Yes' if record['reviewed'] else 'No'}
    Request Date: {record['request_date']}
    Report Date: {record['report_date']}
    """

    st.download_button(
        label="🖨️ Download Printable Summary",
        data=StringIO(summary),
        file_name=f"imaging_report_{record['request_id']}.txt",
        mime="text/plain"
    )
