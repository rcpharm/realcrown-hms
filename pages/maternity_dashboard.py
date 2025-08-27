# Fetch dashboard view
@st.cache_data
def fetch_dashboard():
    return supabase.table("maternity_dashboard_view").select("*").execute().data

data = fetch_dashboard()

# UI
st.title("📊 Maternity Delivery Dashboard")

# Filters
outcomes = sorted(set(d["outcome"] for d in data))
selected_outcome = st.selectbox("Filter by Outcome", ["All"] + outcomes)

filtered = [d for d in data if selected_outcome == "All" or d["outcome"] == selected_outcome]

df = pd.DataFrame(filtered)
df["Delivery Date"] = pd.to_datetime(df["delivery_date"]).dt.strftime("%Y-%m-%d")
st.dataframe(df[[
    "mother_name", "Delivery Date", "delivery_type", "outcome",
    "baby_count", "complications", "delivered_by"
]])
