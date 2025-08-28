import streamlit as st

# 🏥 Page Setup
st.set_page_config(page_title="Real Crown HMS", layout="wide")

# 🔐 Session Initialization
if "user" not in st.session_state:
    st.session_state.user = None
if "option" not in st.session_state:
    st.session_state.option = "Login"
if "redirect_to_dashboard" not in st.session_state:
    st.session_state.redirect_to_dashboard = False

# 🎨 Custom Styles
st.markdown("""
    <style>
        .header-title {
            font-size: 40px;
            font-weight: bold;
            color: #2E8B57;
            margin-bottom: 0;
        }
        .subtitle {
            font-size: 18px;
            color: #555;
            margin-top: 0;
        }
        .credit-box {
            font-size: 13px;
            color: #555;
            background-color: #f9f9f9;
            padding: 12px;
            border-radius: 8px;
            text-align: center;
            margin-top: 40px;
        }
    </style>
""", unsafe_allow_html=True)

# 🏷️ Branding Header
st.markdown("<div class='header-title'>🏥 Real Crown HMS</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Secure access to hospital workflows, staff tools, and patient care modules.</div>", unsafe_allow_html=True)

# 📂 Available Modules
modules = [
    "Dashboard",
    "Patient Records",
    "Appointments",
    "Billing",
    "Prescriptions",
    "Staff Records",
    "Inventory",
    "Reports",
    "Settings"
]

# 🧭 Navigation
if st.session_state.user:
    if st.session_state.redirect_to_dashboard:
        st.session_state.redirect_to_dashboard = False
        st.session_state.option = "Dashboard"

    selected = st.selectbox("📂 Select Module", modules, index=modules.index(st.session_state.option))
    st.session_state.option = selected
else:
    st.session_state.option = "Login"

# 🔐 Access Control
def require_login():
    if not st.session_state.user:
        st.warning("🔒 Please log in to access this section.")
        return False
    return True

def require_role(allowed_roles):
    if not require_login():
        return False
    user = st.session_state.user
    if user["role"] not in allowed_roles:
        st.error("🚫 You do not have permission to access this section.")
        return False
    return True

# 🚦 Routing
option = st.session_state.option

if option == "Login":
    st.switch_page("pages/login.py")

elif option == "Dashboard":
    if require_login():
        st.switch_page("pages/dashboard.py")

elif option == "Patient Records":
    if require_role(["medical_officer", "clinical_officer", "nurse", "admin"]):
        st.switch_page("pages/patient_records.py")

elif option == "Appointments":
    if require_role(["receptionist", "admin"]):
        st.switch_page("pages/appointments.py")

elif option == "Billing":
    if require_role(["accountant", "admin"]):
        st.switch_page("pages/billing.py")

elif option == "Prescriptions":
    if require_role(["medical_officer", "clinical_officer", "admin"]):
        st.switch_page("pages/prescriptions.py")

elif option == "Staff Records":
    if require_role(["admin"]):
        st.switch_page("pages/staff_records.py")

elif option == "Inventory":
    if require_role(["lab_technician", "lab_assistant", "admin"]):
        st.switch_page("pages/inventory.py")

elif option == "Reports":
    if require_role(["admin", "accountant"]):
        st.switch_page("pages/reports.py")

elif option == "Settings":
    if require_role(["admin"]):
        st.switch_page("pages/settings.py")

else:
    st.error("⚠️ Unknown module selected. Returning to Dashboard.")
    st.session_state.option = "Dashboard"
    st.experimental_rerun()

# 🔓 Logout
if st.session_state.user:
    st.markdown("---")
    if st.button("🔓 Logout"):
        st.session_state.clear()
        st.success("You have been logged out.")
        st.experimental_rerun()

# 🧑‍💻 Developer Credit Block
st.markdown("""
    <div class="credit-box">
        <strong>Developed by Sseguya Stephen Jonathan</strong><br>
        📞 Phone: (+256)788739050<br>
        🏢 Powered by <strong>Real Crown Cyber House</strong><br>
        🎯 Sponsored by <strong>Real Crown Initiative</strong><br>
        📧 Email: <a href='mailto:realcrowninitiative@gmail.com'>realcrowninitiative@gmail.com</a>
    </div>
""", unsafe_allow_html=True)
