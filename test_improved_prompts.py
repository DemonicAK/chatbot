#!/usr/bin/env python3
"""
Test script for the improved AI prompt generation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_service import get_role_specific_context, get_tech_specific_context, clean_and_validate_question

def test_role_contexts():
    """Test role-specific context generation"""
    print("=== Testing Role Contexts ===")
    
    roles = [
        "Frontend Developer",
        "Backend Engineer", 
        "Full Stack Developer",
        "DevOps Engineer",
        "Data Scientist",
        "Mobile Developer",
        "Software Engineer"
    ]
    
    for role in roles:
        context = get_role_specific_context(role)
        print(f"\n{role}:")
        print(f"  Focus Areas: {context['focus_areas'][:3]}")
        print(f"  Key Skills: {context['key_skills'][:2]}")
        print(f"  Responsibilities: {context['responsibilities'][:50]}...")

def test_tech_contexts():
    """Test technology-specific context generation"""
    print("\n=== Testing Tech Contexts ===")
    
    technologies = [
        "React", "Python", "PostgreSQL", "AWS", "Docker", 
        "Node.js", "MongoDB", "Kubernetes", "Unknown Technology"
    ]
    
    for tech in technologies:
        context = get_tech_specific_context(tech)
        print(f"\n{tech}:")
        print(f"  Question Types: {context['question_types']}")
        print(f"  Concepts: {context['concepts']}")

def test_question_cleaning():
    """Test question cleaning and validation"""
    print("\n=== Testing Question Cleaning ===")
    
    test_questions = [
        "Here's a question: How do you handle state in React?",
        "1. What is your experience with Python?",
        "• Explain how databases work",
        "How would you optimize a slow query",  # Missing question mark
        "",  # Empty question
        "Q: " + "Very long question " * 20,  # Too long
        "Short?",  # Too short
        "Normal question about React state management?"
    ]
    
    for original in test_questions:
        cleaned = clean_and_validate_question(original, "React", "Frontend Developer", "3-5")
        print(f"\nOriginal: '{original}'")
        print(f"Cleaned:  '{cleaned}'")

def test_experience_mapping():
    """Test experience level mapping"""
    print("\n=== Testing Experience Mapping ===")
    
    # This would normally be in the generate_next_question_ollama function
    experience_levels = ["5", "1-2", "3-5", "5-8", "10+"]
    
    for exp in experience_levels:
        experience_num = int(exp.split('-')[0] if '-' in exp else exp.replace('+', ''))
        if experience_num < 1:
            difficulty_level = "entry-level"
            complexity_desc = "basic concepts, simple implementations, and fundamental understanding"
        elif experience_num < 3:
            difficulty_level = "junior-level"
            complexity_desc = "practical application, debugging skills, and understanding of common patterns"
        elif experience_num < 5:
            difficulty_level = "mid-level"
            complexity_desc = "design decisions, performance considerations, and best practices"
        elif experience_num < 8:
            difficulty_level = "senior-level"
            complexity_desc = "architecture decisions, trade-offs, scalability, and team leadership"
        else:
            difficulty_level = "expert-level"
            complexity_desc = "system design, optimization, mentoring, and industry innovations"
        
        print(f"\n{exp} years -> {difficulty_level}")
        print(f"  Expected: {complexity_desc}")

if __name__ == "__main__":
    test_role_contexts()
    test_tech_contexts()
    test_question_cleaning()
    test_experience_mapping()
    print("\n=== All Tests Complete ===")
