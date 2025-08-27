import streamlit as st
import pandas as pd
from supabase_config import supabase

st.title("Patient Records")

# 🔍 Filters
villages_data = supabase.table("villages").select("id", "name").execute().data
village_map = {v["name"]: v["id"] for v in villages_data}
village_filter = st.selectbox("Filter by Village", ["All"] + list(village_map.keys()))

gender_filter = st.selectbox("Filter by Gender", ["All", "Male", "Female", "Other"])

staff_data = supabase.table("staff").select("id", "full_name").execute().data
staff_map = {s["full_name"]: s["id"] for s in staff_data}
creator_filter = st.selectbox("Filter by Creator", ["All"] + list(staff_map.keys()))

search_name = st.text_input("Search by Name")

# 📦 Fetch patients
query = supabase.table("patients").select(
    "id", "full_name", "age", "gender", "contact_number", "next_of_kin",
    "created_at", "created_by", "village_id"
)

# Apply filters
if village_filter != "All":
    query = query.eq("village_id", village_map[village_filter])
if gender_filter != "All":
    query = query.eq("gender", gender_filter)
if creator_filter != "All":
    query = query.eq("created_by", staff_map[creator_filter])
if search_name:
    query = query.ilike("full_name", f"%{search_name}%")

patients = query.execute().data

# 🧮 Pagination setup
page_size = 10
total = len(patients)
page_num = st.number_input("Page", min_value=1, max_value=max(1, (total - 1) // page_size + 1), step=1)
start = (page_num - 1) * page_size
end = start + page_size
paged_patients = patients[start:end]

# 📄 Export to CSV
if patients:
    df = pd.DataFrame(patients)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "patients.csv", "text/csv")

# 🧾 Display paged results
if paged_patients:
    for p in paged_patients:
        village_name = next((v["name"] for v in villages_data if v["id"] == p["village_id"]), "Unknown")
        creator_name = next((s["full_name"] for s in staff_data if s["id"] == p["created_by"]), "Unknown")

        with st.expander(f"{p['full_name']} ({p['gender']}, {p['age']} yrs)"):
            st.markdown(f"""
            **Contact:** {p['contact_number']}  
            **Next of Kin:** {p['next_of_kin']}  
            **Village:** {village_name}  
            **Created By:** {creator_name}  
            **Registered At:** {p['created_at'][:19].replace("T", " ")}
            """)
else:
    st.info("No patients found with the selected filters.")
