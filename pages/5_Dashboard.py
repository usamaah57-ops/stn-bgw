import streamlit as st
from modules.database import load_services
from modules.alerts import check_alerts
from modules.tracking import get_aircraft_position

st.set_page_config(page_title="Dashboard", page_icon="📊")

st.title("📊 Operations Dashboard")
st.markdown("---")

# Load services
services = load_services()

# Alerts section
st.subheader("⚠️ Operational Alerts")
alerts = check_alerts(services)

if alerts:
    for a in alerts:
        st.warning(a)
else:
    st.success("All required services are completed.")

st.markdown("---")

# Aircraft tracking
st.subheader("✈️ Aircraft Live Tracking")

icao = st.text_input("Enter Aircraft ICAO (hex code)", placeholder="e.g., 0102A3")

if st.button("Track Aircraft"):
    if not icao:
        st.error("Please enter an ICAO code.")
    else:
        data = get_aircraft_position(icao)

        if not data or not data.get("states"):
            st.warning("No live data found for this aircraft.")
        else:
            state = data["states"][0]
            callsign = state[1]
            altitude = state[13]
            velocity = state[9]
            lat = state[6]
            lon = state[5]

            st.success("Aircraft data retrieved successfully.")

            st.write(f"**Callsign:** {callsign}")
            st.write(f"**Altitude:** {altitude} ft")
            st.write(f"**Speed:** {velocity} m/s")
            st.write(f"**Latitude:** {lat}")
            st.write(f"**Longitude:** {lon}")
