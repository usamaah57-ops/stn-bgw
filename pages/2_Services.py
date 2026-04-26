# ------------------------------
# CSS لتلوين حالة الخدمة
# ------------------------------
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
