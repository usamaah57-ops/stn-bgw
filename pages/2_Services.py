import streamlit as st
import os
import datetime
import sys
# ------------------------------
# FIX IMPORT ERROR ON STREAMLIT CLOUD
# ------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# -----------------------------
# FIX IMPORT ERROR ON STREAMLIT CLOUD
# -----------------------------
# This ensures Streamlit can find the "modules" folder even when running from /pages/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.database import save_service, load_services, save_document, load_documents

st.set_page_config(page_title="EgyptAir - Baghdad Station Services", layout="wide")

# -----------------------------
# Header
# -----------------------------
st.markdown("<h2 style='text-align:center;color:#003366;'>EgyptAir – Baghdad Station Services</h2>", unsafe_allow_html=True)
st.markdown("<hr style='border:1px solid #003366;'>", unsafe_allow_html=True)

# Flight info
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    flight = st.text_input("Flight Number:", value="MS123")
with col2:
    reg = st.text_input("Registration:", value="SU-GEH")
with col3:
    date = datetime.date.today().strftime("%d/%m/%Y")
    st.write(f"**Date:** {date}")

# Create folder for uploads
folder_name = f"uploads/{date.replace('/', '-')}-{flight}"
os.makedirs(folder_name, exist_ok=True)

# -----------------------------
# Services list
# -----------------------------
services_list = [
    ("Fuel", "🔥"),
    ("Catering", "🍱"),
    ("Cleaning", "🧹"),
    ("Boarding", "👥"),
    ("Loadsheet", "📄"),
    ("GD", "📋"),
    ("Flight Report", "🛫"),
    ("Load Instruction", "📦"),
    ("Fuel Doc", "⛽"),
    ("Fuel Supply Order", "🧾")
]

# Load existing data
services_data = load_services(flight, date)
docs_data = load_documents(flight, date)

# -----------------------------
# Layout
# -----------------------------
cols = st.columns(5)
for i, (service, icon) in enumerate(services_list):
    with cols[i % 5]:
        st.markdown(f"### {icon} {service}")
        time_val = services_data.get(service, {}).get("time", "--")
        staff_val = services_data.get(service, {}).get("staff", "--")
        st.write(f"**Time:** {time_val}")
        st.write(f"**Staff:** {staff_val}")

        # Register time
        if st.button(f"تسجيل وقت {service}", key=f"log_{service}"):
            time_input = st.time_input(f"وقت الخدمة ({service})", datetime.datetime.now().time(), key=f"time_{service}")
            staff_input = st.text_input(f"اسم الموظف ({service})", key=f"staff_{service}")
            if st.button(f"حفظ {service}", key=f"save_{service}"):
                save_service(flight, reg, date, service, str(time_input), staff_input)
                st.success(f"تم تسجيل {service} بنجاح")

        # Edit time
        if st.button(f"تعديل {service}", key=f"edit_{service}"):
            new_time = st.time_input(f"تعديل الوقت ({service})", datetime.datetime.now().time(), key=f"edit_time_{service}")
            new_staff = st.text_input(f"تعديل الموظف ({service})", key=f"edit_staff_{service}")
            if st.button(f"تأكيد التعديل {service}", key=f"confirm_edit_{service}"):
                save_service(flight, reg, date, service, str(new_time), new_staff)
                st.success(f"تم تعديل {service}")

        # Upload document
        uploaded_file = st.file_uploader(f"رفع مستند {service}", type=["pdf", "jpg", "png"], key=f"upload_{service}")
        if uploaded_file:
            filename = f"{service.lower().replace(' ', '_')}.pdf"
            filepath = os.path.join(folder_name, filename)
            with open(filepath, "wb") as f:
                f.write(uploaded_file.getbuffer())
            save_document(flight, date, service, filename)
            st.success(f"تم رفع مستند {service}")

        # View document
        if service in docs_data:
            st.info(f"📎 مستند مرفوع: {docs_data[service]}")

# -----------------------------
# Auto refresh
# -----------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>تحديث تلقائي كل 10 ثواني</p>", unsafe_allow_html=True)
