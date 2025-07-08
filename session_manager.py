"""
Session state management and utility functions with security enhancements
"""
import streamlit as st
import logging
from config import STEPS, END_KEYWORDS, RETRY_KEYWORDS, RESTART_KEYWORDS, QUESTIONS_PER_TECHNOLOGY, SECURITY_CONFIG
from security.session_security import SecureSessionManager
from security.data_privacy import DataPrivacyManager
from security.encryption import DataEncryption

# Configure logging
logger = logging.getLogger("session_manager")

def initialize_session_state():
    """Initialize session state variables with security features"""
    # Initialize secure session
    SecureSessionManager.initialize_secure_session()
    
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "current_step" not in st.session_state:
        st.session_state["current_step"] = 0
    if "candidate_data" not in st.session_state:
        st.session_state["candidate_data"] = {}
    
    # Initialize encryption if enabled
    if SECURITY_CONFIG.get("enable_encryption", True):
        if "encryption" not in st.session_state:
            st.session_state["encryption"] = DataEncryption()
    
    # Interview state
    if "tech_stack_list" not in st.session_state:
        st.session_state["tech_stack_list"] = []
    if "current_tech_index" not in st.session_state:
        st.session_state["current_tech_index"] = 0
    if "questions_per_tech" not in st.session_state:
        st.session_state["questions_per_tech"] = QUESTIONS_PER_TECHNOLOGY  # Use config value
    if "current_tech_question_count" not in st.session_state:
        st.session_state["current_tech_question_count"] = 0
    if "interview_questions" not in st.session_state:
        st.session_state["interview_questions"] = []
    if "interview_answers" not in st.session_state:
        st.session_state["interview_answers"] = []
    if "previous_question" not in st.session_state:
        st.session_state["previous_question"] = None
    if "previous_answer" not in st.session_state:
        st.session_state["previous_answer"] = None
    if "interview_complete" not in st.session_state:
        st.session_state["interview_complete"] = False
    if "candidate_rating" not in st.session_state:
        st.session_state["candidate_rating"] = {}
    if "overall_rating" not in st.session_state:
        st.session_state["overall_rating"] = ""

def is_end(msg):
    """Check if message is a conversation ending keyword"""
    # Check if the entire message (stripped and lowercased) is exactly an end keyword
    msg_clean = msg.lower().strip()
    return msg_clean in END_KEYWORDS

def is_retry(msg):
    """Check if message is a retry keyword"""
    # Check if the entire message (stripped and lowercased) is exactly a retry keyword
    msg_clean = msg.lower().strip()
    return msg_clean in RETRY_KEYWORDS

def is_restart(msg):
    """Check if message is a restart keyword"""
    # Check if the entire message (stripped and lowercased) is exactly a restart keyword
    msg_clean = msg.lower().strip()
    return msg_clean in RESTART_KEYWORDS
    # return Fa

def reset_conversation():
    """Reset conversation to start"""
    st.session_state["current_step"] = 0
    st.session_state["candidate_data"] = {}
    st.session_state["messages"] = []
    # Reset interview state
    st.session_state["tech_stack_list"] = []
    st.session_state["current_tech_index"] = 0
    st.session_state["questions_per_tech"] = QUESTIONS_PER_TECHNOLOGY
    st.session_state["current_tech_question_count"] = 0
    st.session_state["interview_questions"] = []
    st.session_state["interview_answers"] = []
    st.session_state["previous_question"] = None
    st.session_state["previous_answer"] = None
    st.session_state["interview_complete"] = False
    st.session_state["candidate_rating"] = {}
    st.session_state["overall_rating"] = ""

def add_message(role, content):
    """Add message to chat history"""
    st.session_state["messages"].append({"role": role, "content": content})

def get_current_question():
    """Get current question based on step"""
    if st.session_state["current_step"] < len(STEPS):
        return STEPS[st.session_state["current_step"]]["question"]
    return None

def display_chat_history():
    """Display chat history in Streamlit"""
    for msg in st.session_state["messages"]:
        if msg["role"] == "assistant":
            st.markdown(f"**Assistant:** {msg['content']}")
        else:
            st.markdown(f"**You:** {msg['content']}")

def get_candidate_summary():
    """Get a summary of collected candidate data using secure retrieval"""
    summary = "**Candidate Summary:**\n"
    
    # Use secure data retrieval for sensitive fields
    for step in STEPS:
        key = step["key"]
        value = get_candidate_data_securely(key)
        
        if value:
            if key == "position" and isinstance(value, list):
                summary += f"- {key.title()}: {', '.join(value)}\n"
            else:
                # Mask sensitive data in summary
                if DataPrivacyManager.is_sensitive_field(key):
                    if key == "email":
                        masked_value = DataPrivacyManager.mask_email(value)
                    elif key == "phone":
                        masked_value = DataPrivacyManager.mask_phone_number(value)
                    elif key == "name":
                        masked_value = DataPrivacyManager.mask_name(value)
                    else:
                        masked_value = value
                    summary += f"- {key.title().replace('_', ' ')}: {masked_value}\n"
                else:
                    summary += f"- {key.title().replace('_', ' ')}: {value}\n"
    
    return summary

def prepare_tech_interview():
    """Prepare the technical interview by setting up the tech stack list using secure data"""
    tech_stack = get_candidate_data_securely("tech_stack")
    
    # Parse tech stack into list and clean up
    tech_list = [tech.strip() for tech in tech_stack.split(',') if tech.strip()]
    
    if not tech_list:
        # Fallback if no techs were specified
        tech_list = ["General Programming"]
    
    # Store in session state
    st.session_state["tech_stack_list"] = tech_list
    st.session_state["current_tech_index"] = 0
    st.session_state["current_tech_question_count"] = 0
    
    # Calculate questions per tech (configurable)
    st.session_state["questions_per_tech"] = QUESTIONS_PER_TECHNOLOGY
    
    return tech_list

def get_next_tech_question():
    """Generate and get the next interview question based on tech focus and previous Q&A"""
    try:
        from ai_service import generate_next_question
        
        tech_stack = st.session_state["candidate_data"].get("tech_stack", "")
        tech_list = st.session_state["tech_stack_list"]
        current_tech_index = st.session_state["current_tech_index"]
        
        # Check if we've gone through all technologies
        if current_tech_index >= len(tech_list):
            st.session_state["interview_complete"] = True
            return None
        
        # Get current technology focus
        current_tech = tech_list[current_tech_index]
        
        # Get previous question and answer if they exist
        previous_question = st.session_state["previous_question"]
        previous_answer = st.session_state["previous_answer"]
        
        # Generate the next question
        question = generate_next_question(
            tech_stack,
            tech_focus=current_tech,
            previous_question=previous_question,
            previous_answer=previous_answer
        )
        
        # Ensure we have a valid question
        if not question or len(str(question).strip()) == 0:
            question = f"Can you explain a basic concept in {current_tech}?"
        
        # Format the question with tech focus for display and storage
        formatted_question = f"[{current_tech}] {question}"
        
        # Store the formatted question (this is what will be used for evaluation)
        st.session_state["interview_questions"].append(formatted_question)
        st.session_state["previous_question"] = question  # Store raw question for follow-up generation
        
        return formatted_question
        
    except Exception as e:
        logger.error(f"Error in get_next_tech_question: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        
        # Return a fallback question
        current_tech = st.session_state["tech_stack_list"][st.session_state["current_tech_index"]] if st.session_state["tech_stack_list"] else "programming"
        fallback_question = f"[{current_tech}] Can you explain a basic concept in {current_tech}? [Error occurred during generation]"
        
        # Still store it for consistency
        st.session_state["interview_questions"].append(fallback_question)
        st.session_state["previous_question"] = fallback_question
        
        return fallback_question

def store_interview_answer(answer):
    """Store candidate's answer and prepare for next question"""
    # Store the answer
    st.session_state["interview_answers"].append(answer)
    st.session_state["previous_answer"] = answer
    
    # Update counters
    st.session_state["current_tech_question_count"] += 1
    
    # Check if we should move to the next technology
    if st.session_state["current_tech_question_count"] >= st.session_state["questions_per_tech"]:
        st.session_state["current_tech_index"] += 1
        st.session_state["current_tech_question_count"] = 0
        st.session_state["previous_question"] = None
        st.session_state["previous_answer"] = None
    
    # Check if interview is complete
    if st.session_state["current_tech_index"] >= len(st.session_state["tech_stack_list"]):
        st.session_state["interview_complete"] = True
        return True
    
    return False

def get_question_answer_pairs():
    """Get pairs of questions and answers for evaluation"""
    pairs = []
    for i, question in enumerate(st.session_state["interview_questions"]):
        if i < len(st.session_state["interview_answers"]):
            pairs.append({
                "question": question,
                "answer": st.session_state["interview_answers"][i]
            })
    return pairs

def store_candidate_rating(rating_data):
    """Store the rating data for the candidate"""
    st.session_state["candidate_rating"] = rating_data
    
def store_overall_rating(rating):
    """Store the overall rating for the candidate"""
    st.session_state["overall_rating"] = rating

def is_technicalinterview_in_progress():
    """Check if the technical interview is in progress"""
    # Check if we have tech_stack_list populated and the interview isn't complete
    return (len(st.session_state["tech_stack_list"]) > 0 and 
            not st.session_state["interview_complete"])

def is_interview_complete():
    """Check if the technical interview is complete"""
    return st.session_state["interview_complete"]

def get_rating_display():
    """Get HTML for displaying the candidate rating"""
    if not st.session_state["candidate_rating"]:
        return ""
    
    rating_html = "<div style='background-color: #1e1e1e; color: white; padding: 20px; border-radius: 10px; margin-top: 20px; border: 1px solid #333;'>"
    rating_html += "<h3 style='color: white; margin-top: 0;'>Candidate Evaluation</h3>"
    
    # Add skill ratings
    rating_html += "<h4 style='color: white; margin-bottom: 10px;'>Technical Skills Assessment:</h4>"
    rating_html += "<ul style='color: white; margin: 0; padding-left: 20px;'>"
    for skill, score in st.session_state["candidate_rating"].items():
        # Convert numerical score to stars for visual appeal
        stars = "★" * int(score) + "☆" * (5 - int(score))
        rating_html += f"<li style='color: white; margin-bottom: 5px;'><strong style='color: white;'>{skill}:</strong> <span style='color: #ffd700;'>{stars}</span> <span style='color: #ccc;'>({score}/5)</span></li>"
    rating_html += "</ul>"
    
    # Add overall rating with appropriate color (brighter colors for dark background)
    overall = st.session_state["overall_rating"]
    color_map = {
        "Very Strong Hire": "#4CAF50",  # Bright green
        "Strong Hire": "#66BB6A",       # Light green
        "OK Hire": "#FFC107",           # Amber
        "Weak Hire": "#FF9800",         # Orange
        "Bad Hire": "#F44336"           # Red
    }
    color = color_map.get(overall, "#B0B0B0")
    
    rating_html += f"<h4 style='color: white; margin-bottom: 10px; margin-top: 20px;'>Overall Recommendation:</h4>"
    rating_html += f"<div style='font-size: 18px; font-weight: bold; color: {color}; padding: 10px; background-color: rgba(0,0,0,0.1); border-radius: 5px; text-align: center;'>{overall}</div>"
    logger.info(f"Overall rating stored: {overall}")
    rating_html += "</div>"
    
    return rating_html

def store_candidate_data_securely(key: str, value: str):
    """Securely store candidate data with encryption if enabled"""
    try:
        if SECURITY_CONFIG.get("enable_encryption", True) and hasattr(st.session_state, "encryption"):
            encryption = st.session_state.encryption
            
            # Encrypt sensitive fields
            if DataPrivacyManager.is_sensitive_field(key):
                encrypted_value = encryption.encrypt_data(value)
                st.session_state["candidate_data"][key] = encrypted_value
                # Store whether this field is encrypted
                if "encrypted_fields" not in st.session_state:
                    st.session_state["encrypted_fields"] = set()
                st.session_state["encrypted_fields"].add(key)
                
                # Log anonymized version
                anonymized_data = DataPrivacyManager.anonymize_for_logging({key: value})
                logger.info(f"Stored encrypted data: {anonymized_data}")
            else:
                # Non-sensitive data can be stored as-is
                st.session_state["candidate_data"][key] = value
        else:
            # Fallback to regular storage
            st.session_state["candidate_data"][key] = value
            
    except Exception as e:
        logger.error(f"Error storing candidate data securely: {e}")
        # Fallback to regular storage
        st.session_state["candidate_data"][key] = value

def get_candidate_data_securely(key: str) -> str:
    """Securely retrieve candidate data with decryption if needed"""
    try:
        if key not in st.session_state["candidate_data"]:
            return ""
            
        value = st.session_state["candidate_data"][key]
        
        # Check if this field was encrypted
        encrypted_fields = st.session_state.get("encrypted_fields", set())
        if key in encrypted_fields and hasattr(st.session_state, "encryption"):
            encryption = st.session_state.encryption
            return encryption.decrypt_data(value)
        else:
            return value
            
    except Exception as e:
        logger.error(f"Error retrieving candidate data securely: {e}")
        # Fallback to returning raw value
        return st.session_state["candidate_data"].get(key, "")
