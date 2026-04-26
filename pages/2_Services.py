import streamlit as st
import os
import datetime
import sys

# -----------------------------------
# FIX IMPORT ERROR ON STREAMLIT CLOUD
# -----------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from modules.database import save_service, load_services

st.set_page_config(page_title="EgyptAir - Baghdad Station Services", layout="wide")

# -----------------------------------
# Background Image
# -----------------------------------
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
background-image: url("assets/egyptair_bg.jpg");
background-size: cover;
background-repeat: no-repeat;
background-attachment: fixed;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}
[data-testid="stSidebar"] {{
background: rgba(255,255,255,0.85);
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# -----------------------------------
# CSS for icons + status colors
# -----------------------------------
st.markdown("""
<style>
.service-box {
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 10px;
    color: black;
    font-weight: bold;
}
.status-red {
    background-color: rgba(255, 0, 0, 0.25);
}
.status-yellow {
    background-color: rgba(255, 255, 0, 0.35);
}
.status-green {
    background-color: rgba(0, 255, 0, 0.25);
}
.service-icon {
    font-size: 22px !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# Header
# -----------------------------------
st.markdown("<h2 style='text-align:center;color:#003366;'>EgyptAir – Baghdad Station Services</h2>", unsafe_allow_html=True)
st.markdown("<hr style='border:1px solid #003366;'>", unsafe_allow_html=True)

# -----------------------------------
# Flight Info
# -----------------------------------
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    flight = st.text_input("Flight Number:", value="MS628")
with col2:
    reg = st.text_input("Registration:", value="SU-GEH")
with col3:
    date = datetime.date.today().strftime("%d/%m/%Y")
    st.write(f"Date: {date}")

# -----------------------------------
# CLEAN SERVICE LIST (NO DUPLICATES)
# -----------------------------------
services_list = [
    ("CHOCKS_ON", "🟢"),
    ("AFT_OPEN", "🔓"),
    ("AFT_CLOSE", "🔒"),
    ("FWD_OPEN", "🔓"),
    ("FWD_CLOSE", "🔒"),
    ("CLEANING", "🧹"),
    ("FUEL", "⛽"),
    ("FIRST_PAX", "👥"),
    ("LAST_PAX", "👤"),
    ("LOADSHEET", "📄"),
    ("CLOSE_DOOR", "🚪"),
    ("PUSHBACK_TRUCK", "🚛"),
    ("PUSH_BACK", "🛫")
]

services_data = load_services(flight, date)

# -----------------------------------
# Display Services in Grid Layout
# -----------------------------------
cols = st.columns(4)

for i, (service, icon) in enumerate(services_list):

    start_time = services_data.get(service, {}).get("start", None)
    end_time = services_data.get(service, {}).get("end", None)

    # Determine status color
    if start_time is None and end_time is None:
        status_class = "status-red"      # Not started
    elif start_time is not None and end_time is None:
        status_class = "status-yellow"   # In progress
    else:
        status_class = "status-green"    # Completed

    with cols[i % 4]:

        # Service header box
        st.markdown(
            f"<div class='service-box {status_class}'>"
            f"<span class='service-icon'>{icon}</span> {service}"
            f"</div>",
            unsafe_allow_html=True
        )

        st.write(f"Arrival (Start): {start_time if start_time else '--'}")
        st.write(f"End Time: {end_time if end_time else '--'}")

        notes_val = services_data.get(service, {}).get("notes", "--")
        st.write(f"Notes: {notes_val}")

        # Start button
        if st.button(f"Record Start {service}", key=f"start_{service}"):
            t = st.time_input(f"Start Time ({service})", datetime.datetime.now().time(), key=f"time_start_{service}")
            n = st.text_area(f"Notes ({service})", key=f"notes_start_{service}")
            save_service(flight, reg, date, service, str(t), n, mode="start")
            st.success(f"Start time recorded for {service}")

        # End button
        if st.button(f"Record End {service}", key=f"end_{service}"):
            t = st.time_input(f"End Time ({service})", datetime.datetime.now().time(), key=f"time_end_{service}")
            n = st.text_area(f"Notes ({service})", key=f"notes_end_{service}")
            save_service(flight, reg, date, service, str(t), n, mode="end")
            st.success(f"End time recorded for {service}")

# -----------------------------------
# Auto Refresh
# -----------------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>Auto-refresh every 10 seconds</p>", unsafe_allow_html=True)
