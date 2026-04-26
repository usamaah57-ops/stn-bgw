import streamlit as st
from modules.database import load_archive

st.set_page_config(page_title="Archive", page_icon="📦")

st.title("📦 Archived Flights")
st.markdown("---")

records = load_archive()

if not records:
    st.info("No archived flights yet.")
else:
    st.subheader("Archived Records")

    for r in records:
        flight, reg, date, key, time, staff = r

        with st.expander(f"{date} — {flight} — {reg}"):
            st.write(f"**Service:** {key}")
            st.write(f"**Time:** {time}")
            st.write(f"**Staff:** {staff}")
