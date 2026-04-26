import streamlit as st
from modules.backup import backup_database
from modules.database import clear_services

st.set_page_config(page_title="Settings", page_icon="⚙️")

st.title("⚙️ System Settings")
st.markdown("---")

st.subheader("Database Backup")
if st.button("Create Backup"):
    try:
        backup_database()
        st.success("Backup created successfully.")
    except:
        st.error("Backup failed. Make sure the database exists.")

st.markdown("---")

st.subheader("Clear Current Services")
if st.button("Clear Services"):
    clear_services()
    st.success("All current services have been cleared.")

st.markdown("---")

st.subheader("System Info")
st.write("EgyptAir – Baghdad Station Operations System")
st.write("Developed for operational workflow automation.")
