"""
Main conversation processing logic with security enhancements
"""
import streamlit as st
import logging
from config import STEPS, DATABASE_CONFIG
from session_manager import (
    is_end, is_retry, is_restart, reset_conversation, add_message,
    get_current_question, get_next_tech_question, prepare_tech_interview,
    store_interview_answer, is_technicalinterview_in_progress, is_interview_complete,
    get_question_answer_pairs, store_candidate_rating, store_overall_rating,
    store_candidate_data_securely, get_candidate_data_securely
)
from ai_service import rate_candidate_responses
from security.session_security import SecureSessionManager
from security.data_privacy import DataPrivacyManager
from database.models import interview_data_manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("conversation_handler")

def process_user_input(user_input):
    """Process user input and handle validation with security checks"""
    # Validate session security first
    if not SecureSessionManager.validate_session():
        return
    
    # Sanitize input for security
    user_input = DataPrivacyManager.sanitize_for_storage({"input": user_input})["input"]
    
    # Log anonymized input for debugging
    anonymized_input = user_input[:50] + "..." if len(user_input) > 50 else user_input
    logger.info(f"Processing anonymized input: {anonymized_input}")
    # Check for special commands
    # if is_end(user_input):
    #     if is_technicalinterview_in_progress():
    #         # Complete the interview if in progress
    #         add_message("assistant", "Interview ended early. Let me evaluate your responses so far...")
    #         complete_interview()
    #     else:
    #         add_message("assistant", "Thank you for your time! We'll review your information and contact you with next steps. Goodbye!")
    #     return
    
    # if is_restart(user_input):
    #     reset_conversation()
    #     add_message("assistant", "Let's start over! What's your full name?")
    #     return
    
    # if is_retry(user_input):
    #     question = get_current_question()
    #     if question:
    #         add_message("assistant", f"Sure! {question}")
    #     return
    
    # Check if we're in the technical interview phase
    if is_technicalinterview_in_progress():
        # Store the answer and check if interview is complete
        interview_complete = store_interview_answer(user_input)
        
        if interview_complete:
            # If all questions are answered, complete the interview
            complete_interview()
        else:
            # Ask the next question
            next_question = get_next_tech_question()
            if next_question:
                add_message("assistant", f"Thanks for your answer. Next question:\n\n{next_question}")
            else:
                # Should not happen, but just in case
                complete_interview()
        return
    
    # Process current step if not in interview
    current_step = st.session_state["current_step"]
    
    if current_step < len(STEPS):
        step_config = STEPS[current_step]
        validator = step_config["validator"]
        key = step_config["key"]
        
            # Handle other validations (returns 2 values)
        is_valid, error_msg = validator(user_input)
        if is_valid:
            # Use secure storage
            store_candidate_data_securely(key, user_input.strip())
            st.session_state["current_step"] += 1
            next_question = get_current_question()
            if next_question:
                add_message("assistant", f"Thank you! {next_question}")
                is_valid, error_msg = validator(user_input)
                if key == "tech_stack":
                    if is_valid:
                        # Use secure storage
                        store_candidate_data_securely(key, user_input.strip())
                        st.session_state["current_step"] += 1
                        # If tech stack is set, prepare for technical interview
                        st.session_state["is_technicalinterview_in_progress"] = True
                        start_technical_interview()
            else:
                # Generate technical questions
                start_technical_interview()
        else:
            add_message("assistant", f"{error_msg} Please try again, or type 'retry' to see the question again, or 'restart' to start over.")
    else:
        # If interview is already complete, just acknowledge
        if is_interview_complete():
            add_message("assistant", "Thank you! Your interview is complete and we've evaluated your responses. Type 'exit' to end the chat.")
        else:
            # Should not happen normally, but start the interview if we reach here
            start_technical_interview()

def start_technical_interview():
    """Start the technical interview process by preparing tech stack and generating first question"""
    try:
        tech_stack = st.session_state["candidate_data"].get("tech_stack", "")
        experience = st.session_state["candidate_data"].get("experience", "")
        
        logger.info(f"Starting technical interview with tech_stack: '{tech_stack}' and experience: '{experience}'")
        
        # Prepare tech list and interview structure
        tech_list = prepare_tech_interview()
        logger.info(f"Prepared interview with {len(tech_list)} technologies: {tech_list}")
        
        # Get the first question
        first_question = get_next_tech_question()
        logger.info(f"Generated first question: '{first_question}'")
        
        if first_question and len(str(first_question).strip()) > 0:
            # Introduction to technical interview
            intro_message = f"Great! Now I'll ask you some technical questions based on your {experience} years of experience with {tech_stack}. I'll focus on each technology in your stack, with follow-up questions to understand your knowledge depth.\n\n"
            intro_message += f"First question:\n\n{first_question}"
        else:
            logger.warning(f"Failed to generate the first question or question is empty: '{first_question}'")
            intro_message = "It seems I couldn't generate proper questions. Let's end the interview."
        
        add_message("assistant", intro_message)
        logger.info("Technical interview started successfully")
        
    except Exception as e:
        logger.error(f"Error in start_technical_interview: {str(e)}")
        add_message("assistant", f"Sorry, there was an error starting the technical interview: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

def complete_interview():
    """Complete the interview process and evaluate the candidate"""
    # Get all question-answer pairs
    qa_pairs = get_question_answer_pairs()
    
    if not qa_pairs:
        add_message("assistant", "There were no questions answered. Let's end the interview.")
        return
    
    # Get the tech stack and experience
    tech_stack = st.session_state["candidate_data"].get("tech_stack", "")
    experience_level = st.session_state["candidate_data"].get("experience", "")
    interested_role = st.session_state["candidate_data"].get("position", "Software Engineer")
    
    # Rate the candidate's responses
    add_message("assistant", "Thank you for completing the technical interview. I'm now evaluating your responses...")
    
    # Get ratings from AI
    rating_result = rate_candidate_responses(tech_stack, qa_pairs, interested_role, experience_level)
    ratings = rating_result.get("ratings", {})
    overall = rating_result.get("overall", "Error in rating process")
    
    # Store ratings
    store_candidate_rating(ratings)
    store_overall_rating(overall)
    
    # Save all data to database if enabled
    if DATABASE_CONFIG.get("save_to_database", True) and interview_data_manager:
        try:
            if not interview_data_manager.is_available():
                logger.warning("Database not configured - skipping data save")
                add_message("assistant", "⚠️ Database not configured. Interview complete but data not saved to database.")
            else:
                add_message("assistant", "Saving your interview data securely...")
                
                # Get all candidate data
                candidate_data = st.session_state.get("candidate_data", {})
                
                # Save to database with encryption
                interview_id = interview_data_manager.save_complete_interview(
                    candidate_data=candidate_data,
                    qa_pairs=qa_pairs,
                    ratings=ratings,
                    overall_rating=overall
                )
                
                if interview_id:
                    logger.info(f"Successfully saved interview data to database with ID: {interview_id}")
                    # Store interview ID in session for reference
                    st.session_state["interview_id"] = interview_id
                    add_message("assistant", "✅ Your interview data has been saved securely to our database.")
                else:
                    logger.error("Failed to save interview data to database")
                    add_message("assistant", "⚠️ There was an issue saving your data to our database, but your interview is complete.")
                
        except Exception as e:
            logger.error(f"Database save error: {e}")
            add_message("assistant", "⚠️ There was an issue saving your data to our database, but your interview is complete.")
    
    # Create a summary message
    rating_message = "## Interview Evaluation\n\n"
    rating_message += "Based on your responses to the technical questions, here's my assessment:\n\n"
    
    # Add individual skill ratings
    rating_message += "### Technical Skills\n"
    for skill, score in ratings.items():
        stars = "★" * score + "☆" * (5 - score)
        rating_message += f"- **{skill}**: {stars} ({score}/5)\n"
    
    # Add overall recommendation
    rating_message += f"\n### Overall Recommendation: **{overall}**\n\n"
    rating_message += "Thank you for participating in this interview. You can type 'exit' to end the chat."
    
    # Add the message to the chat
    add_message("assistant", rating_message)
# ...existing code...
