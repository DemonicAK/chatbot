#!/usr/bin/env python3
"""
Simple test script to check question generation
"""
from ai_service import generate_next_question_ollama

def test_question_generation():
    print("Testing question generation...")
    
    tech_stack = "python"
    experience_level = "1"
    interested_role = "Software Engineer"
    tech_focus = "python"
    
    try:
        question = generate_next_question_ollama(
            tech_stack=tech_stack,
            experience_level=experience_level,
            interested_role=interested_role,
            previous_question=None,
            previous_answer=None,
            tech_focus=tech_focus
        )
        
        print(f"Generated question: '{question}'")
        print("Question generation successful!")
        
    except Exception as e:
        print(f"Error generating question: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_question_generation()
