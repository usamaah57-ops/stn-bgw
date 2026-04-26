import streamlit as st
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from modules.database import clear_services, init_db

st.set_page_config(page_title="Settings", layout="wide")

st.markdown("<h2 style='text-align:center;color:#003366;'>Settings – EgyptAir Baghdad Station</h2>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# زر لمسح كل الخدمات
if st.button("🗑️ Clear All Services"):
    clear_services()
    st.success("All services have been cleared successfully!")

# زر لإعادة تهيئة قاعدة البيانات
if st.button("🔄 Reset Database"):
    init_db()
    st.success("Database has been reset successfully!")
