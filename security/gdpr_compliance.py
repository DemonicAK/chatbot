"""
GDPR compliance utilities
"""
import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class GDPRCompliance:
    """Handle GDPR compliance features"""
    
    @staticmethod
    def show_privacy_notice() -> bool:
        """Display privacy notice and get consent"""
        st.markdown("### 🔒 Privacy Notice")
        
        with st.expander("📋 Data Collection & Privacy Information - Please Read", expanded=True):
            st.markdown("""
            **What data we collect:**
            - Personal information: Name, email, phone number, location
            - Professional information: Experience, position preferences, tech stack
            - Conversation data: Your responses during this interview
            
            **How we use your data:**
            - To evaluate your candidacy for positions
            - To match you with suitable job opportunities
            - To improve our recruitment process
            
            **Your rights under GDPR:**
            - ✅ Right to access your data
            - ✅ Right to correct inaccurate data
            - ✅ Right to delete your data
            - ✅ Right to data portability
            - ✅ Right to object to processing
            
            **Data security:**
            - All sensitive data is encrypted
            - Data is stored securely and access is limited
            - We comply with GDPR and data protection regulations
            - Data will be automatically deleted after 30 days unless you're hired
            
            **Contact:** For any privacy concerns, contact our Data Protection Officer at privacy@talentscout.com
            """)
        
        consent = st.checkbox(
            "✅ I consent to the collection and processing of my data as described above",
            key="privacy_consent"
        )
        
        if consent:
            # Log consent in session
            GDPRCompliance.log_consent()
            return True
        else:
            st.warning("⚠️ Please accept the privacy notice to continue with the interview.")
            return False
    
    @staticmethod
    def log_consent():
        """Log user consent in session state"""
        if 'consent_data' not in st.session_state:
            st.session_state.consent_data = {
                'consent_given': True,
                'consent_timestamp': datetime.now().isoformat(),
                'session_id': st.session_state.get('session_id', 'unknown')
            }
            logger.info(f"Consent logged for session: {st.session_state.get('session_id', 'unknown')}")
    
    @staticmethod
    def has_valid_consent() -> bool:
        """Check if user has given valid consent"""
        return st.session_state.get('consent_data', {}).get('consent_given', False)
    
    @staticmethod
    def show_data_rights_info():
        """Show information about data rights"""
        st.sidebar.markdown("### 🛡️ Your Data Rights")
        st.sidebar.markdown("""
        Under GDPR, you have the right to:
        - Access your data
        - Correct your data
        - Delete your data
        - Object to processing
        
        Contact: privacy@talentscout.com
        """)
    
    @staticmethod
    def schedule_data_deletion(retention_days: int = 30) -> datetime:
        """Schedule automatic data deletion"""
        deletion_date = datetime.now() + timedelta(days=retention_days)
        if 'data_retention' not in st.session_state:
            st.session_state.data_retention = {
                'deletion_scheduled': deletion_date.isoformat(),
                'retention_days': retention_days
            }
        return deletion_date
    
    @staticmethod
    def show_data_deletion_info():
        """Show information about data deletion schedule"""
        if 'data_retention' in st.session_state:
            deletion_date = st.session_state.data_retention.get('deletion_scheduled')
            if deletion_date:
                try:
                    deletion_dt = datetime.fromisoformat(deletion_date)
                    st.sidebar.info(f"🗑️ Data will be automatically deleted on: {deletion_dt.strftime('%Y-%m-%d')}")
                except ValueError:
                    pass
