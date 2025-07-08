"""
Utility functions for the chatbot
"""
import streamlit as st
from session_manager import get_candidate_summary, get_rating_display, is_interview_complete
from ai_service import get_ai_status, set_ai_provider, get_current_ai_provider
from config import AI_PROVIDERS

def create_sidebar():
    """Create a sidebar with candidate information and controls"""
    with st.sidebar:
        st.header("🤖 AI Configuration")
        
        # AI Provider Status
        ai_status = get_ai_status()
        current_provider = get_current_ai_provider()
        
        # Display Ollama status
        ollama_status = ai_status.get("ollama", {})
        if ollama_status.get("available"):
            st.success(f"✅ Llama 3.1 8B: {ollama_status['message']}")
        else:
            st.error(f"❌ Llama 3.1 8B: {ollama_status['message']}")
        
        # If Ollama is not available, show setup instructions
        if not ollama_status.get("available"):
            with st.expander("🔧 Setup Ollama"):
                st.markdown("""
                **To use Llama 3.1 8B:**
                1. Install Ollama: `curl -fsSL https://ollama.ai/install.sh | sh`
                2. Start Ollama: `ollama serve`
                3. Pull Llama 3.1 8B: `ollama pull llama3.1:8b`
                4. Refresh this page
                
                **Check installation:**
                - `ollama list` - See installed models
                - `ollama ps` - See running models
                """)
        
        # Show available models button
        if st.button("🔄 Refresh Status"):
            st.rerun()
        
        st.divider()
        
        st.header("📋 Candidate Information")
        
        # Display current step
        current_step = st.session_state.get("current_step", 0)
        total_steps = 7
        progress = current_step / total_steps
        st.progress(progress)
        st.write(f"Step {current_step + 1} of {total_steps}")
        
        # Display collected data
        if st.session_state.get("candidate_data"):
            st.subheader("Collected Data")
            data = st.session_state["candidate_data"]
            for key, value in data.items():
                if key == "position" and isinstance(value, list):
                    st.write(f"**{key.title()}:** {', '.join(value)}")
                else:
                    st.write(f"**{key.title().replace('_', ' ')}:** {value}")
        
        # Display candidate rating if interview is complete
        if is_interview_complete() and st.session_state.get("candidate_rating"):
            st.divider()
            st.subheader("🎯 Candidate Rating")
            
            # Display ratings for each skill
            for skill, rating in st.session_state["candidate_rating"].items():
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.write(f"**{skill}:**")
                with col2:
                    stars = "★" * rating + "☆" * (5 - rating)
                    st.write(f"{stars} ({rating}/5)")
            
            # Display overall rating with appropriate color
            st.divider()
            overall = st.session_state.get("overall_rating", "")
            
            if overall:
                # Map ratings to colors
                color_map = {
                    "Very Strong Hire": "green",
                    "Strong Hire": "green",
                    "OK Hire": "orange",
                    "Weak Hire": "orange",
                    "Bad Hire": "red"
                }
                color = color_map.get(overall, "gray")
                
                st.markdown(f"### Overall: <span style='color:{color}'>{overall}</span>", unsafe_allow_html=True)
        
        # Control buttons
        st.subheader("🎛️ Controls")
        if st.button("Clear Chat"):
            st.session_state["messages"] = []
            st.rerun()
        
        if st.button("Reset Conversation"):
            st.session_state["current_step"] = 0
            st.session_state["candidate_data"] = {}
            st.session_state["messages"] = []
            st.session_state["interview_questions"] = []
            st.session_state["interview_answers"] = []
            st.session_state["current_question_index"] = 0
            st.session_state["interview_complete"] = False
            st.session_state["candidate_rating"] = {}
            st.session_state["overall_rating"] = ""
            st.rerun()

def display_help():
    """Display help information"""
    with st.expander("ℹ️ Help & Commands"):
        st.markdown("""
        **Available Commands:**
        - `exit`, `quit`, `bye`, `end` - End the conversation
        - `retry`, `try again` - Repeat the current question
        - `restart`, `start over` - Start from the beginning
        
        **Input Requirements:**
        - **Name:** Only letters and spaces
        - **Email:** Valid email format (e.g., user@example.com)
        - **Phone:** Exactly 10 digits
        - **Experience:** Whole numbers only (0-50)
        - **Position:** Comma-separated values (e.g., "Developer, Analyst")
        - **Location:** Any text
        - **Tech Stack:** Any text describing your technologies
        
        **AI Provider:**
        - **Llama 3.1 8B (Ollama):** Local model, requires Ollama installation
        - Completely private - no data leaves your machine
        - Free to use after installation
        """)

def display_ai_info():
    """Display AI provider information"""
    ai_status = get_ai_status()
    ollama_status = ai_status.get("ollama", {})
    
    if ollama_status.get("available"):
        st.info("🤖 Currently using: **Llama 3.1 8B (Local)**")
    else:
        st.warning("⚠️ Ollama not available. Please set up Ollama to use the chatbot.")
        
    # Display candidate rating if interview complete
    if is_interview_complete():
        rating_html = get_rating_display()
        if rating_html:
            st.markdown(rating_html, unsafe_allow_html=True)

def export_candidate_data():
    """Export candidate data as JSON"""
    import json
    data = st.session_state.get("candidate_data", {})
    
    # Include interview data if available
    if st.session_state.get("interview_questions") and st.session_state.get("interview_answers"):
        data["technical_interview"] = {
            "questions": st.session_state["interview_questions"],
            "answers": st.session_state["interview_answers"]
        }
    
    # Include ratings if available
    if st.session_state.get("candidate_rating"):
        data["ratings"] = {
            "skills": st.session_state["candidate_rating"],
            "overall": st.session_state.get("overall_rating", "")
        }
    
    if data:
        return json.dumps(data, indent=2)
    return None

def send_candidate_report_email():
    """Send candidate report via email"""
    import json
    data = st.session_state.get("candidate_data", {})
    
    if not data:
        return False, "No candidate data to send"
    
    try:
        # Get candidate name and position
        name = data.get("name", "Candidate")
        position = data.get("position", ["Unknown Position"])
        if isinstance(position, list):
            position = ", ".join(position)
        
        # Build email subject
        subject = f"Interview Report: {name} for {position}"
        
        # Build email body
        body = f"# Interview Report for {name}\n\n"
        
        # Basic information
        body += "## Candidate Information\n"
        for key, value in data.items():
            if key == "position" and isinstance(value, list):
                body += f"- **{key.title()}:** {', '.join(value)}\n"
            else:
                body += f"- **{key.title().replace('_', ' ')}:** {value}\n"
        
        # Technical interview
        if st.session_state.get("interview_questions") and st.session_state.get("interview_answers"):
            body += "\n## Technical Interview\n"
            for i, question in enumerate(st.session_state["interview_questions"]):
                if i < len(st.session_state["interview_answers"]):
                    body += f"\n### Q{i+1}: {question}\n"
                    body += f"**Answer:** {st.session_state['interview_answers'][i]}\n"
        
        # Ratings
        if st.session_state.get("candidate_rating"):
            body += "\n## Skills Assessment\n"
            for skill, rating in st.session_state["candidate_rating"].items():
                stars = "★" * rating + "☆" * (5 - rating)
                body += f"- **{skill}:** {stars} ({rating}/5)\n"
            
            # Overall rating
            overall = st.session_state.get("overall_rating", "")
            if overall:
                body += f"\n## Overall Recommendation: **{overall}**\n"
        
        # Mock sending email (for future implementation)
        # In a real system, you would connect to an email service here
        
        return True, f"Report for {name} would be sent in a real implementation"
    except Exception as e:
        return False, f"Error preparing report: {str(e)}"
