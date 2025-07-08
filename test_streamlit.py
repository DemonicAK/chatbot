#!/usr/bin/env python3
"""
Simple Streamlit test to isolate the question display issue
"""
import streamlit as st
from ai_service import generate_next_question_ollama

st.title("Question Generation Test")

if st.button("Generate Question"):
    with st.spinner("Generating question..."):
        try:
            question = generate_next_question_ollama(
                tech_stack="python",
                experience_level="1",
                interested_role="Software Engineer",
                previous_question=None,
                previous_answer=None,
                tech_focus="python"
            )
            
            st.success(f"Generated question: {question}")
            
        except Exception as e:
            st.error(f"Error: {e}")
            import traceback
            st.code(traceback.format_exc())
