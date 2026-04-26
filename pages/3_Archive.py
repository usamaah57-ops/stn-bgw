import streamlit as st
import os
import sys
from fpdf import FPDF   # مكتبة لإنشاء PDF

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from modules.database import load_archive, init_db

st.set_page_config(page_title="EgyptAir - Archive", layout="wide")

# تأكد أن قاعدة البيانات موجودة
init_db()

st.markdown("<h2 style='text-align:center;color:#003366;'>Archive – EgyptAir Baghdad Station</h2>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# Load archive data
rows = load_archive()

if not rows:
    st.warning("Archive is empty.")
else:
    # Show table
    st.table(rows)

    # Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="EgyptAir Baghdad Station Archive", ln=True, align="C")
    pdf.ln(10)

    for flight, reg, date, service, start, end in rows:
        pdf.cell(200, 10, txt=f"Flight: {flight} | Reg: {reg} | Date: {date} | Service: {service} | Start: {start} | End: {end}", ln=True)

    # Save PDF to file
    pdf_file = "archive.pdf"
    pdf.output(pdf_file)

    # Provide download button
    with open(pdf_file, "rb") as f:
        st.download_button("Download Archive PDF", f, file_name="archive.pdf", mime="application/pdf")
