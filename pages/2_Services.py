import streamlit as st
from modules.auth import login
from modules.database import load_services, save_service, clear_services, archive_services
from modules.utils import format_time

st.set_page_config(page_title="Services", page_icon="🛠️")

st.title("🛠️ Service Registration")
st.markdown("---")

# Login
staff = login()

st.subheader(f"Logged in as: **{staff}**")
st.markdown("---")

services = load_services()

# Service list
service_keys = {
    "FUEL_ARRIVAL": "Fuel Arrival",
    "FUEL_START": "Fuel Start",
    "FUEL_END": "Fuel End",
    "CATERING": "Catering",
    "CLEANING": "Cleaning",
    "BOARDING_START": "Boarding Start",
    "BOARDING_END": "Boarding End",
    "LOADSHEET": "Loadsheet Completed",
    "CLOSE_DOOR": "Doors Closed"
}

st.subheader("Record a Service")

selected_service = st.selectbox("Select Service", list(service_keys.keys()))
time_input = st.time_input("Select Time")
time_str = time_input.strftime("%H:%M")

if st.button("Save Service"):
    save_service(selected_service, time_str, staff)
    st.success(f"{service_keys[selected_service]} recorded at {time_str}")
    st.rerun()

st.markdown("---")

# Display current services
st.subheader("Current Services")

if services:
    for key, data in services.items():
        st.write(f"**{service_keys[key]}** — {format_time(data['time'])} — {data['staff']}")
else:
    st.info("No services recorded yet.")

st.markdown("---")

# Archive section
st.subheader("Archive Flight Services")

flight = st.text_input("Flight Number (e.g., MSR123)")
reg = st.text_input("Aircraft Registration (e.g., SU-GEX)")

if st.button("Archive Flight"):
    if flight and reg:
        success = archive_services(flight, reg)
        if success:
            st.success("Flight archived successfully.")
            clear_services()
            st.rerun()
        else:
            st.warning("This flight is already archived today.")
    else:
        st.error("Please enter both flight and registration.")
