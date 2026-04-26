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
    # Show table in Streamlit
    st.table(rows)

    # Generate PDF with table
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    # عنوان
    pdf.cell(200, 10, txt="EgyptAir Baghdad Station Archive", ln=True, align="C")
    pdf.ln(10)

    # رأس الجدول
    pdf.set_font("Arial", 'B', 10)
    headers = ["Flight", "Reg", "Date", "Service", "Start", "End"]
    col_widths = [25, 25, 25, 40, 25, 25]

    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 10, header, border=1, align="C")
    pdf.ln()

    # محتوى الجدول مع ألوان
    pdf.set_font("Arial", size=9)
    for flight, reg, date, service, start, end in rows:
        # تحديد اللون حسب الحالة
        if start and end:
            pdf.set_fill_color(144, 238, 144)  # أخضر فاتح
        elif start and not end:
            pdf.set_fill_color(255, 255, 153)  # أصفر فاتح
        else:
            pdf.set_fill_color(255, 182, 193)  # أحمر فاتح

        pdf.cell(col_widths[0], 8, str(flight), border=1, fill=True)
        pdf.cell(col_widths[1], 8, str(reg), border=1, fill=True)
        pdf.cell(col_widths[2], 8, str(date), border=1, fill=True)
        pdf.cell(col_widths[3], 8, str(service), border=1, fill=True)
        pdf.cell(col_widths[4], 8, str(start) if start else "--", border=1, fill=True)
        pdf.cell(col_widths[5], 8, str(end) if end else "--", border=1, fill=True)
        pdf.ln()

    # Save PDF to file
    pdf_file = "archive.pdf"
    pdf.output(pdf_file)

    # Provide download button
    with open(pdf_file, "rb") as f:
        st.download_button("Download Archive PDF", f, file_name="archive.pdf", mime="application/pdf")
