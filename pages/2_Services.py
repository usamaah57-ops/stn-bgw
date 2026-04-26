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

from modules.database import save_service, load_services

st.set_page_config(page_title="EgyptAir - Baghdad Station Services", layout="wide")

# ------------------------------
# خلفية مصر للطيران
# ------------------------------
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
background-image: url("images/egyptair_bg.jpg");
background-size: cover;
background-repeat: no-repeat;
background-attachment: fixed;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}
[data-testid="stSidebar"] {{
background: rgba(255,255,255,0.85);
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# ------------------------------
# Header
# ------------------------------
st.markdown("<h2 style='text-align:center;color:#003366;'>EgyptAir – Baghdad Station Services</h2>", unsafe_allow_html=True)
st.markdown("<hr style='border:1px solid #003366;'>", unsafe_allow_html=True)

# Flight info
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    flight = st.text_input("Flight Number:", value="MS628")
with col2:
    reg = st.text_input("Registration:", value="SU-GEH")
with col3:
    date = datetime.date.today().strftime("%d/%m/%Y")
    st.write(f"**Date:** {date}")

# ------------------------------
# الخدمات التشغيلية
# ------------------------------
services_list = [
    ("CHOCKS_ON", "🟢"),
    ("AFT_OPEN", "🔓"),
    ("FWD_OPEN", "🔓"),
    ("CLEANING_START", "🧹"),
    ("FUEL_ARRIVAL", "⛽"),
    ("FUEL_END", "✅"),
    ("AFT_CLOSE", "🔒"),
    ("CLEANING_END", "🧼"),
    ("FIRST_PAX", "👥"),
    ("PUSHBACK_TRUCK", "🚛"),
    ("LOADSHEET", "📄"),
    ("FWD_CLOSE", "🔒"),
    ("LAST_PAX", "👤"),
    ("CLOSE_DOOR", "🚪"),
    ("PUSH_BACK", "🛫")
]

services_data = load_services(flight, date)
cols = st.columns(5)

for i, (service, icon) in enumerate(services_list):
    with cols[i % 5]:
        st.markdown(f"### {icon} {service}")
        time_val = services_data.get(service, {}).get("time", "--")
        notes_val = services_data.get(service, {}).get("notes", "--") if "notes" in services_data.get(service, {}) else "--"
        st.write(f"**Time:** {time_val}")
        st.write(f"**Notes:** {notes_val}")

        if st.button(f"تسجيل وقت {service}", key=f"log_{service}"):
            time_input = st.time_input(f"وقت الخدمة ({service})", datetime.datetime.now().time(), key=f"time_{service}")
            notes_input = st.text_area(f"ملاحظات ({service})", key=f"notes_{service}")
            if st.button(f"حفظ {service}", key=f"save_{service}"):
                save_service(flight, reg, date, service, str(time_input), notes_input)
                st.success(f"تم تسجيل {service} بنجاح")

        if st.button(f"تعديل {service}", key=f"edit_{service}"):
            new_time = st.time_input(f"تعديل الوقت ({service})", datetime.datetime.now().time(), key=f"edit_time_{service}")
            new_notes = st.text_area(f"تعديل الملاحظات ({service})", key=f"edit_notes_{service}")
            if st.button(f"تأكيد التعديل {service}", key=f"confirm_edit_{service}"):
                save_service(flight, reg, date, service, str(new_time), new_notes)
                st.success(f"تم تعديل {service}")

# ------------------------------
# Auto refresh
# ------------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>تحديث تلقائي كل 10 ثواني</p>", unsafe_allow_html=True)
