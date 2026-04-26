from fpdf import FPDF
from io import BytesIO

def generate_basic_report(flight, reg, date, records):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Baghdad Station Operations Report", ln=True, align="C")

    pdf.set_font("Arial", "", 12)
    pdf.ln(5)
    pdf.cell(0, 8, f"Flight: {flight}", ln=True)
    pdf.cell(0, 8, f"Registration: {reg}", ln=True)
    pdf.cell(0, 8, f"Date: {date}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(60, 8, "Service", border=1)
    pdf.cell(40, 8, "Time", border=1)
    pdf.cell(80, 8, "Staff", border=1, ln=True)

    pdf.set_font("Arial", "", 11)
    for r in records:
        pdf.cell(60, 8, r[3], border=1)
        pdf.cell(40, 8, r[4], border=1)
        pdf.cell(80, 8, r[5], border=1, ln=True)

    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    buffer = BytesIO(pdf_bytes)
    buffer.seek(0)
    return buffer
