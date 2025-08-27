import streamlit as st

# 🌟 Branding and Header
st.markdown("""
    <style>
        .title {
            font-size: 36px;
            font-weight: bold;
            color: #2E8B57;
        }
        .credit {
            font-size: 13px;
            color: #555;
            margin-top: 20px;
            line-height: 1.6;
            background-color: #f9f9f9;
            padding: 10px;
            border-radius: 8px;
        }
    </style>
    <div class="title">🏥 Real Crown HMS — Staff Dashboard</div>
""", unsafe_allow_html=True)

# ✅ Check login
if "user" not in st.session_state:
    st.warning("🔒 You must log in first.")
    st.stop()

user = st.session_state["user"]
name = user.get("name", "Unknown")
role = user.get("role", "guest")

# 🎉 Welcome Message
st.markdown(f"""
    <div style='background-color:#dff0d8;padding:10px;border-radius:8px;margin-top:10px'>
        <strong>Welcome, {name}</strong> <span style='color:#555'>({role})</span>
    </div>
""", unsafe_allow_html=True)

# 🎯 Role-Based Panels
def show_panel(title, description, color="#e6f7ff"):
    st.markdown(f"""
        <div style='background-color:{color};padding:15px;border-radius:10px;margin-top:20px'>
            <h4 style='color:#333'>{title}</h4>
            <p style='color:#555'>{description}</p>
        </div>
    """, unsafe_allow_html=True)

# 🧭 Dashboard Content
role_panels = {
    "admin": ("Admin Panel", "Manage staff accounts, configure system settings, and view reports."),
    "medical_officer": ("Medical Officer Dashboard", "Access patient records, prescribe medication, and oversee clinical operations."),
    "clinical_officer": ("Clinical Officer Dashboard", "Review patient history, conduct examinations, and coordinate with medical officers."),
    "receptionist": ("Receptionist Dashboard", "Register patients, manage appointments, and handle front desk operations."),
    "nurse": ("Nurse Dashboard", "Monitor patient vitals, assist in procedures, and update medical charts."),
    "midwife": ("Midwife Dashboard", "Manage maternal care, assist in deliveries, and provide postnatal support."),
    "lab_technician": ("Lab Technician Dashboard", "Conduct lab tests, manage samples, and report results."),
    "lab_assistant": ("Lab Assistant Dashboard", "Support lab technicians, prepare equipment, and handle documentation."),
    "sonographer": ("Sonographer Dashboard", "Perform ultrasound scans and assist in diagnostic imaging."),
    "radiographer": ("Radiographer Dashboard", "Conduct X-rays and other radiographic procedures."),
    "accountant": ("Accountant Dashboard", "Manage billing, financial records, and generate reports.")
}

if role in role_panels:
    title, desc = role_panels[role]
    show_panel(title, desc)
else:
    show_panel("General Access", "Your role does not have specific dashboard features yet.", color="#fff3cd")

# 🧑‍💻 Developer Credit Block
st.markdown("""
    <div class="credit">
        <strong>Developed by Sseguya Stephen Jonathan</strong><br>
        📞 Phone: (+256)788739050<br>
        🏢 Powered by Real Crown Cyber House<br>
        🎯 Sponsored by Real Crown Initiative<br>
        📧 Email: <a href='mailto:realcrowninitiative@gmail.com'>realcrowninitiative@gmail.com</a>
    </div>
""", unsafe_allow_html=True)
