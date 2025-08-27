import streamlit as st
import streamlit.components.v1 as components

# ─────────────────────────────────────────────────────────────
# 🔰 Developer Credit Banner
banner_html = """
<div style="background-color:#0f1117; padding:6px 0; overflow:hidden;">
  <marquee behavior="scroll" direction="left" scrollamount="5" style="color:#ffffff; font-size:14px;">
    Developed by <strong>Sseguya Stephen Jonathan</strong> &nbsp; 📞 Phone: (+256)788739050 &nbsp; 🏢 Powered by Real Crown Cyber House &nbsp; 🎯 Sponsored by Real Crown Initiative &nbsp; 📧 Email: realcrowninitiative@gmail.com
  </marquee>
</div>
"""
components.html(banner_html, height=40)

# ─────────────────────────────────────────────────────────────
# ⚙️ Page Config
st.set_page_config(page_title="Real Crown HMS", layout="wide")

# ─────────────────────────────────────────────────────────────
# 🧭 Sidebar Navigation
st.sidebar.title("🧭 Navigation")
section = st.sidebar.radio("Go to", [
    "Dashboard",
    "Login",
    "Register",
    "Patient Registration",
    "Patient View",
    "Patient Edit",
    "Visit Log",
    "Visit Details",
    "Diagnosis & Medication",
    "Medication History",
    "Prescription Logger",
    "Pharmacy Dispensation",
    "Lab Request",
    "Lab Register",
    "Lab Results",
    "Lab Inventory",
    "Imaging Request",
    "Imaging Register",
    "Imaging Result Logger",
    "ANC Visit Logger",
    "ANC Schedule Tracker",
    "Delivery Logger",
    "Newborn Registration",
    "Maternity Dashboard",
    "Accounting Dashboard",
    "Staff List"
])

# ─────────────────────────────────────────────────────────────
# 🔗 Page Routing
page_map = {
    "Dashboard": "pages/dashboard.py",
    "Login": "pages/login.py",
    "Register": "pages/register.py",
    "Patient Registration": "pages/patient_register.py",
    "Patient View": "pages/patient_view.py",
    "Patient Edit": "pages/patient_edit.py",
    "Visit Log": "pages/visit_log.py",
    "Visit Details": "pages/visit_details.py",
    "Diagnosis & Medication": "pages/diagnosis_medication.py",  # You can rename this file if needed
    "Medication History": "pages/medication_history_viewer.py",
    "Prescription Logger": "pages/prescription_logger.py",
    "Pharmacy Dispensation": "pages/pharmacy_dispensation_register.py",
    "Lab Request": "pages/lab_request.py",
    "Lab Register": "pages/lab_register.py",
    "Lab Results": "pages/lab_results.py",
    "Lab Inventory": "pages/lab_inventory.py",
    "Imaging Request": "pages/Imaging_request.py",
    "Imaging Register": "pages/imaging_register_dashboard.py",
    "Imaging Result Logger": "pages/imaging_result_logger.py",
    "ANC Visit Logger": "pages/anc_visit_logger.py",
    "ANC Schedule Tracker": "pages/anc_schedule_tracker.py",
    "Delivery Logger": "pages/delivery_logger.py",
    "Newborn Registration": "pages/newborn_registration.py",
    "Maternity Dashboard": "pages/maternity_dashboard.py",
    "Accounting Dashboard": "pages/accounting_dashboard.py",
    "Staff List": "pages/staff_list.py"
}

# Switch to selected page
if section in page_map:
    st.switch_page(page_map[section])
else:
    st.error("🚧 Page not found or not yet implemented.")
