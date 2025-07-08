#!/usr/bin/env python3
"""
Simple test script for the improved AI prompt generation
"""

try:
    from ai_service import get_role_specific_context, get_tech_specific_context, clean_and_validate_question
    
    print("=== Testing Role Context ===")
    context = get_role_specific_context("Frontend Developer")
    print(f"Frontend Developer context: {context}")
    
    print("\n=== Testing Tech Context ===")
    tech_context = get_tech_specific_context("React")
    print(f"React context: {tech_context}")
    
    print("\n=== Testing Question Cleaning ===")
    original = "Here's a question: How do you handle state in React?"
    cleaned = clean_and_validate_question(original, "React", "Frontend Developer", "3-5")
    print(f"Original: {original}")
    print(f"Cleaned: {cleaned}")
    
    print("\n=== All Tests Passed ===")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
