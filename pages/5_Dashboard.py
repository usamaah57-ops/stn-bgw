import streamlit as st
import os
import sys
import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from modules.database import load_services, init_db

st.set_page_config(page_title="Operations Dashboard", layout="wide")

# تأكد أن قاعدة البيانات موجودة
init_db()

st.markdown("<h2 style='text-align:center;color:#003366;'>Operations Dashboard – EgyptAir Baghdad Station</h2>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# اختيار الرحلة والتاريخ
col1, col2 = st.columns([1, 1])
with col1:
    flight = st.text_input("Flight Number:", value="MS628")
with col2:
    date = datetime.date.today().strftime("%d/%m/%Y")

# تحميل البيانات
services = load_services(flight, date)

if not services:
    st.warning("No services recorded for this flight/date.")
else:
    st.success(f"Showing services for Flight {flight} on {date}")

    # عرض جدول الخدمات
    table_data = []
    for service, times in services.items():
        table_data.append({
            "Service": service,
            "Start": times.get("start", "--"),
            "End": times.get("end", "--")
        })
    st.table(table_data)

    # إحصائيات مبسطة
    total_services = len(services)
    completed = sum(1 for s in services.values() if s.get("start") and s.get("end"))
    in_progress = sum(1 for s in services.values() if s.get("start") and not s.get("end"))
    not_started = sum(1 for s in services.values() if not s.get("start") and not s.get("end"))

    st.markdown("### Service Status Summary")
    col
