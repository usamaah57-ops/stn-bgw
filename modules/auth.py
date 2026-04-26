import streamlit as st

def login():
    # Initialize session state
    if 'staff_confirmed' not in st.session_state:
        st.session_state.staff_confirmed = False

    if 'current_staff' not in st.session_state:
        st.session_state.current_staff = ""

    # If staff not confirmed, show login box
    if not st.session_state.staff_confirmed:
        name_input = st.text_input("Enter your full name:")
        if st.button("Confirm and Enter"):
            if name_input.strip():
                st.session_state.current_staff = name_input.strip()
                st.session_state.staff_confirmed = True
                st.rerun()
            else:
                st.error("Please enter your name to continue.")
        st.stop()

    # Return logged-in staff name
    return st.session_state.current_staff
