import streamlit as st
from supabase_config import supabase
from datetime import datetime
import pandas as pd

st.title("🧪 Lab Inventory Management")

# 👤 Staff attribution
staff_data = supabase.table("staff").select("id", "full_name").execute().data
staff_names = {s["full_name"]: s["id"] for s in staff_data}
updated_by_name = st.selectbox("Updated by", list(staff_names.keys()))
updated_by_id = staff_names[updated_by_name]

# 📦 Add new inventory item
st.subheader("➕ Add or Update Item")
item_name = st.text_input("Item Name")
category = st.selectbox("Category", ["Reagent", "Consumable", "Equipment", "Other"])
quantity = st.number_input("Quantity", min_value=0)
unit = st.text_input("Unit (e.g. ml, strips, boxes)")

if st.button("Save Item"):
    if item_name and quantity and unit:
        timestamp = datetime.now().isoformat()
        data = {
            "item_name": item_name,
            "category": category,
            "quantity": quantity,
            "unit": unit,
            "last_updated": timestamp,
            "updated_by": updated_by_id
        }
        response = supabase.table("lab_inventory").insert(data).execute()
        if response.status_code == 201:
            st.success(f"Item '{item_name}' saved successfully.")
        else:
            st.error("Failed to save item.")
    else:
        st.warning("Please fill in all required fields.")

# 📊 View inventory
st.subheader("📋 Current Inventory")
inventory_data = supabase.table("lab_inventory").select("*").execute().data
if inventory_data:
    df = pd.DataFrame(inventory_data)
    df["last_updated"] = pd.to_datetime(df["last_updated"]).dt.strftime("%Y-%m-%d %H:%M")
    st.dataframe(df)

    # 📤 Export
    st.download_button("Download CSV", df.to_csv(index=False), "lab_inventory.csv", "text/csv")
else:
    st.info("No inventory data available.")
