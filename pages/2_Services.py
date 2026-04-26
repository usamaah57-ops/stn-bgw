import streamlit as st
import os
import datetime
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from modules.database import save_service, load_services, init_db

st.set_page_config(page_title="EgyptAir - Baghdad Station Services", layout="wide")

# Initialize DB
init_db()

# Background Image
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
background-image: url("assets/egyptair_bg.jpg");
background-size: cover;
background-repeat: no-repeat;
background-attachment: fixed;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# CSS
st.markdown("""
<style>
.service-box {
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 10px;
    color: black;
    font-weight: bold;
}
.status-red { background-color: rgba(255, 0, 0, 0.25); }
.status-yellow { background-color: rgba(255, 255, 0, 0.35); }
.status-green { background-color: rgba(0, 255, 0, 0.25); }
.service-icon { font-size: 22px !important; }
</style>
""", unsafe_allow_html
