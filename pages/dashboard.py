import streamlit as st

st.title("Staff Dashboard")

# Check if user is logged in
if "user" not in st.session_state:
    st.warning("You must log in first.")
    st.stop()

user = st.session_state["user"]
role = user["role"]
name = user["name"]

st.success(f"Welcome, {name} ({role})")

# Role-based dashboard content
if role == "admin":
    st.subheader("Admin Panel")
    st.write("Manage staff accounts, configure system settings, and view reports.")

elif role == "medical_officer":
    st.subheader("Medical Officer Dashboard")
    st.write("Access patient records, prescribe medication, and oversee clinical operations.")

elif role == "clinical_officer":
    st.subheader("Clinical Officer Dashboard")
    st.write("Review patient history, conduct examinations, and coordinate with medical officers.")

elif role == "receptionist":
    st.subheader("Receptionist Dashboard")
    st.write("Register patients, manage appointments, and handle front desk operations.")

elif role == "nurse":
    st.subheader("Nurse Dashboard")
    st.write("Monitor patient vitals, assist in procedures, and update medical charts.")

elif role == "midwife":
    st.subheader("Midwife Dashboard")
    st.write("Manage maternal care, assist in deliveries, and provide postnatal support.")

elif role == "lab_technician":
    st.subheader("Lab Technician Dashboard")
    st.write("Conduct lab tests, manage samples, and report results.")

elif role == "lab_assistant":
    st.subheader("Lab Assistant Dashboard")
    st.write("Support lab technicians, prepare equipment, and handle documentation.")

elif role == "sonographer":
    st.subheader("Sonographer Dashboard")
    st.write("Perform ultrasound scans and assist in diagnostic imaging.")

elif role == "radiographer":
    st.subheader("Radiographer Dashboard")
    st.write("Conduct X-rays and other radiographic procedures.")

elif role == "accountant":
    st.subheader("Accountant Dashboard")
    st.write("Manage billing, financial records, and generate reports.")

else:
    st.subheader("General Access")
    st.write("Your role does not have specific dashboard features yet.")
 
