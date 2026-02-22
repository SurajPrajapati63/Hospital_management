import streamlit as st
import sys
from pathlib import Path

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Hospital Management System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# Configure Session State
# ----------------------------
if "user" not in st.session_state:
    st.session_state.user = None

if "access_token" not in st.session_state:
    st.session_state.access_token = None

if "refresh_token" not in st.session_state:
    st.session_state.refresh_token = None

# ----------------------------
# Sidebar Navigation
# ----------------------------
with st.sidebar:
    st.title("🏥 Hospital Management System")
    
    if st.session_state.user:
        st.success(f"Logged in as: {st.session_state.user.get('full_name', 'Unknown')}")
        st.write(f"Role: {st.session_state.user.get('role', 'Unknown')}")
        
        if st.button("Logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.access_token = None
            st.session_state.refresh_token = None
            st.rerun()
        
        st.divider()
        
        page = st.radio("Navigation", [
            "📊 Dashboard",
            "👥 Patients",
            "👨‍⚕️ Doctors",
            "📅 Appointments",
            "💊 Prescriptions",
            "💳 Billing",
            "🤖 AI Assistant",
            "📈 Analytics"
        ])
    else:
        st.warning("Please log in to continue")
        page = "🔐 Login"

# ----------------------------
# Main Content Area
# ----------------------------
if page == "🔐 Login":
    st.title("Hospital Management System - Login")
    st.write("Please enter your credentials to login")
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login", use_container_width=True):
        if email and password:
            st.info("Login functionality integration pending...")
        else:
            st.error("Please enter email and password")

elif not st.session_state.user:
    st.warning("Please log in to access this page")

else:
    if page == "📊 Dashboard":
        st.title("Dashboard")
        st.write("Dashboard content coming soon...")
    
    elif page == "👥 Patients":
        st.title("Patients Management")
        st.write("Patients management content coming soon...")
    
    elif page == "👨‍⚕️ Doctors":
        st.title("Doctors Management")
        st.write("Doctors management content coming soon...")
    
    elif page == "📅 Appointments":
        st.title("Appointments")
        st.write("Appointments content coming soon...")
    
    elif page == "💊 Prescriptions":
        st.title("Prescriptions")
        st.write("Prescriptions content coming soon...")
    
    elif page == "💳 Billing":
        st.title("Billing")
        st.write("Billing content coming soon...")
    
    elif page == "🤖 AI Assistant":
        st.title("AI Medical Assistant")
        st.write("AI Assistant content coming soon...")
    
    elif page == "📈 Analytics":
        st.title("Analytics")
        st.write("Analytics content coming soon...")