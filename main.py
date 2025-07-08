"""
TalentScout Hiring Assistant Chatbot with Security Features
Main Streamlit application
"""
import streamlit as st
from config import INITIAL_GREETING, SECURITY_CONFIG, PRIVACY_CONFIG
from session_manager import (
    initialize_session_state, add_message, display_chat_history, is_interview_complete
)
from conversation_handler import process_user_input
from utils import create_sidebar, display_help, display_ai_info, send_candidate_report_email
from security.session_security import SecureSessionManager
from security.gdpr_compliance import GDPRCompliance

def main():
    """Main application function with security features"""
    st.set_page_config(page_title="TalentScout Hiring Assistant", page_icon="🤖")
    st.title("🤖 TalentScout Hiring Assistant Chatbot")
    
    # Initialize session state with security
    initialize_session_state()
    
    # Validate session security
    if not SecureSessionManager.validate_session():
        return
    
    # Show GDPR compliance notice if required
    if PRIVACY_CONFIG.get("privacy_notice_required", True):
        if not GDPRCompliance.has_valid_consent():
            if not GDPRCompliance.show_privacy_notice():
                st.stop()
    
    # Create sidebar with security info
    create_sidebar()
    
    # Show session info and data rights
    SecureSessionManager.show_session_info()
    GDPRCompliance.show_data_rights_info()
    GDPRCompliance.show_data_deletion_info()
    
    # Display AI provider info
    display_ai_info()
    
    # Display help
    display_help()
    
    # Initial greeting
    if not st.session_state["messages"]:
        add_message("assistant", INITIAL_GREETING)
    
    # Display chat history
    display_chat_history()
    
    # Add email report button if interview is complete
    if is_interview_complete() and st.session_state.get("candidate_rating"):
        if st.button("📧 Send Candidate Report"):
            success, message = send_candidate_report_email()
            if success:
                st.success(message)
            else:
                st.error(message)
    
    # User input form
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Your message:", key="user_input")
        submit_button = st.form_submit_button("Send")
    
    # Process user input
    if submit_button and user_input:
        add_message("user", user_input)
        process_user_input(user_input)
        st.rerun()

if __name__ == "__main__":
    main()
