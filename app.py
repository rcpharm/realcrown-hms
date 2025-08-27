import streamlit as st

# 🌟 Page Config
st.set_page_config(page_title="Real Crown HMS Dashboard", layout="wide")

# 🎨 Custom Styles
st.markdown("""
    <style>
        .title {
            font-size: 36px;
            font-weight: bold;
            color: #2E8B57;
            margin-bottom: 0;
        }
        .subtitle {
            font-size: 18px;
            color: #555;
            margin-top: 0;
        }
        .credit {
            font-size: 13px;
            color: #555;
            margin-top: 30px;
            line-height: 1.6;
            background-color: #f9f9f9;
            padding: 12px;
            border-radius: 8px;
            text-align: center;
        }
        .panel {
            background-color: #e6f7ff;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            box-shadow: 0 0 5px rgba(0,0,0,0.05);
        }
        .panel-warning {
            background-color: #fff3cd;
        }
    </style>
""", unsafe_allow_html=True)

# 🏥 Header
st.markdown("<div class='title'>🏥 Real Crown HMS — Staff Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Secure access to clinical workflows, staff tools, and patient care modules.</div>", unsafe_allow_html=True)

# 🔐 Session Check
if "user" not in st.session_state:
    st.warning("🔒 You must log in first.")
    st.stop()

user = st.session_state["user"]
name = user.get("name", "Unknown")
role = user.get("role", "guest")

# 🎉 Welcome Message
st.markdown(f"""
    <div style='background-color:#dff0d8;padding:12px;border-radius:8px;margin-top:20px'>
        <strong>Welcome, {name}</strong> <span style='color:#555'>({role})</span>
    </div>
""", unsafe_allow_html=True)

# 🎯 Role-Based Panels
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

# 🧭 Display Panel
if role in role_panels:
    title, desc = role_panels[role]
    st.markdown(f"""
        <div class='panel'>
            <h4>{title}</h4>
            <p>{desc}</p>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
        <div class='panel panel-warning'>
            <h4>General Access</h4>
            <p>Your role does not have specific dashboard features yet.</p>
        </div>
    """, unsafe_allow_html=True)

# 🧑‍💻 Developer Credit Block
st.markdown("""
    <div class="credit">
        <strong>Developed by Sseguya Stephen Jonathan</strong><br>
        📞 Phone: (+256)788739050<br>
        🏢 Powered by <strong>Real Crown Cyber House</strong><br>
        🎯 Sponsored by <strong>Real Crown Initiative</strong><br>
        📧 Email: <a href='mailto:realcrowninitiative@gmail.com'>realcrowninitiative@gmail.com</a>
    </div>
""", unsafe_allow_html=True)
