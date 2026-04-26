import streamlit as st
from modules.database import load_archive
from modules.pdf_generator import generate_basic_report

st.set_page_config(page_title="Reports", page_icon="📄")

st.title("📄 Generate PDF Reports")
st.markdown("---")

records = load_archive()

if not records:
    st.info("No archived flights available for reporting.")
    st.stop()

# Group records by flight/date
grouped = {}
for r in records:
    flight, reg, date, key, time, staff = r
    group_key = f"{date} — {flight} — {reg}"
    if group_key not in grouped:
        grouped[group_key] = []
    grouped[group_key].append(r)

selected = st.selectbox("Select Flight Report", list(grouped.keys()))

if st.button("Generate PDF"):
    data = grouped[selected]
    flight = data[0][0]
    reg = data[0][1]
    date = data[0][2]

    pdf_buffer = generate_basic_report(flight, reg, date, data)

    st.success("PDF generated successfully.")
    st.download_button(
        label="Download PDF",
        data=pdf_buffer,
        file_name=f"{flight}_{date.replace('/', '-')}.pdf",
        mime="application/pdf"
    )
