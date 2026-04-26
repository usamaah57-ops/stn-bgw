import streamlit as st
import os
from datetime import date

st.set_page_config(page_title="DOC1", page_icon="📂")

st.title("📂 DOC1 - المستندات")

# إدخال بيانات الرحلة
flight_number = st.text_input("✈️ رقم الرحلة")
flight_date = st.date_input("📅 تاريخ الرحلة", value=date.today())

if flight_number and flight_date:
    archive_folder = f"archive/{flight_number}_{flight_date}"
    os.makedirs(archive_folder, exist_ok=True)

    def save_document(doc_name, uploaded_file):
        if uploaded_file is not None:
            file_path = f"{archive_folder}/{doc_name}.pdf"
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"✅ تم حفظ {doc_name} في {file_path}")
        else:
            st.warning("⚠️ الرجاء رفع أو تصوير المستند")

    st.subheader("اختر المستند المطلوب:")

    # الصف الأول من الأيقونات
    col1, col2, col3 = st.columns(3)
    with col1:
        uploaded_loadsheet = st.file_uploader("📄 Load Sheet", type=["pdf","jpg","png"])
        if st.button("حفظ Load Sheet"):
            save_document("load_sheet", uploaded_loadsheet)

    with col2:
        uploaded_instruction = st.file_uploader("📋 Load Instruction", type=["pdf","jpg","png"])
        if st.button("حفظ Load Instruction"):
            save_document("load_instruction", uploaded_instruction)

    with col3:
        uploaded_gd = st.file_uploader("🗒️ G.D", type=["pdf","jpg","png"])
        if st.button("حفظ G.D"):
            save_document("gd", uploaded_gd)

    # الصف الثاني من الأيقونات
    col4, col5, col6 = st.columns(3)
    with col4:
        uploaded_fuelinfo = st.file_uploader("⛽ Fuel Info", type=["pdf","jpg","png"])
        if st.button("حفظ Fuel Info"):
            save_document("fuel_info", uploaded_fuelinfo)

    with col5:
        uploaded_fuelreceived = st.file_uploader("🧾 Fuel Received", type=["pdf","jpg","png"])
        if st.button("حفظ Fuel Received"):
            save_document("fuel_received", uploaded_fuelreceived)

    with col6:
        uploaded_report = st.file_uploader("📈 Flight Report", type=["pdf","jpg","png"])
        if st.button("حفظ Flight Report"):
            save_document("flight_report", uploaded_report)
