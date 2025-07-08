"""
Secure session management utilities
"""
import streamlit as st
import uuid
import time
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class SecureSessionManager:
    """Handle secure session management"""
    
    @staticmethod
    def initialize_secure_session():
        """Initialize secure session with unique ID and timestamp"""
        if 'session_id' not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())
            st.session_state.session_start = time.time()
            logger.info(f"New secure session initialized: {st.session_state.session_id}")
        
        if 'security_initialized' not in st.session_state:
            st.session_state.security_initialized = True
            logger.info("Security features initialized")
    
    @staticmethod
    def clear_sensitive_data():
        """Clear sensitive data from session"""
        sensitive_keys = [
            'candidate_data', 'interview_answers', 'interview_questions',
            'previous_answer', 'tech_stack_list'
        ]
        
        cleared_keys = []
        for key in sensitive_keys:
            if key in st.session_state:
                del st.session_state[key]
                cleared_keys.append(key)
        
        if cleared_keys:
            logger.info(f"Cleared sensitive data: {cleared_keys}")
    
    @staticmethod
    def is_session_expired(timeout_minutes: int = 30) -> bool:
        """Check if session has expired"""
        if 'session_start' not in st.session_state:
            return True
        
        elapsed = time.time() - st.session_state.session_start
        return elapsed > (timeout_minutes * 60)
    
    @staticmethod
    def refresh_session():
        """Refresh session timestamp"""
        st.session_state.session_start = time.time()
    
    @staticmethod
    def get_session_info() -> dict:
        """Get session information for logging"""
        return {
            'session_id': st.session_state.get('session_id', 'unknown'),
            'session_start': st.session_state.get('session_start', 0),
            'session_age_minutes': (time.time() - st.session_state.get('session_start', time.time())) / 60
        }
    
    @staticmethod
    def handle_session_expiry():
        """Handle expired session"""
        st.warning("⏰ Your session has expired for security reasons. Please restart the conversation.")
        SecureSessionManager.clear_sensitive_data()
        
        # Reset to initial state
        st.session_state.current_step = 0
        st.session_state.messages = []
        st.session_state.interview_complete = False
        
        # Show restart button
        if st.button("🔄 Start New Session"):
            # Clear all session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    @staticmethod
    def show_session_info():
        """Show session information in sidebar"""
        session_info = SecureSessionManager.get_session_info()
        st.sidebar.markdown("### 🔒 Session Info")
        st.sidebar.markdown(f"**Session ID:** `{session_info['session_id'][:8]}...`")
        st.sidebar.markdown(f"**Active for:** {session_info['session_age_minutes']:.1f} minutes")
        
        # Show warning if session is close to expiring
        if session_info['session_age_minutes'] > 25:  # 5 minutes before 30-minute timeout
            st.sidebar.warning("⚠️ Session will expire soon")
    
    @staticmethod
    def validate_session() -> bool:
        """Validate current session and handle expiry"""
        if SecureSessionManager.is_session_expired():
            SecureSessionManager.handle_session_expiry()
            return False
        else:
            SecureSessionManager.refresh_session()
            return True
