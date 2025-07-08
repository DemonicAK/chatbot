# Candidate Assessment Feature

This document describes the implementation of the candidate assessment and rating feature in the TalentScout Hiring Assistant Chatbot.

## Feature Overview

The new assessment feature enables the chatbot to:

1. Ask technical questions specific to the candidate's tech stack and experience level
2. Record and analyze the candidate's answers
3. Rate each skill in the candidate's tech stack on a scale of 1-5
4. Provide an overall hiring recommendation (Very Strong Hire, Strong Hire, OK Hire, Weak Hire, Bad Hire)
5. Display the assessment in the UI
6. Allow sending the assessment report via email

## Implementation Details

### Technical Question Generation

- Questions are generated using Ollama (Llama 3.1) based on:
  - The candidate's tech stack (languages, frameworks, etc.)
  - The candidate's experience level
- The difficulty of questions adapts to the candidate's experience
- Questions are parsed and presented one by one

### Interview Flow

1. Basic candidate information is collected (name, email, experience, etc.)
2. Technical questions are generated and asked sequentially
3. Candidate answers are recorded for each question
4. After all questions are answered (or if the interview is ended early), an assessment is generated

### Assessment and Rating

- Each skill in the tech stack is rated on a scale of 1-5
- Ratings are displayed visually using stars (★★★☆☆)
- An overall hiring recommendation is provided
- Assessment is displayed in both the chat and the sidebar
- A button to send the assessment via email is provided when the interview is complete

### Rating Categories

The overall hiring recommendation falls into one of these categories:
- Very Strong Hire
- Strong Hire
- OK Hire
- Weak Hire
- Bad Hire

## Technical Implementation

New functionality was added to:

- `ai_service.py`: Added functions to generate experience-specific questions and rate candidate responses
- `session_manager.py`: Added state management for interview questions, answers, and ratings
- `conversation_handler.py`: Updated to handle the interview flow and assessment
- `utils.py`: Added functions to display ratings and send reports
- `main.py`: Added a button to send the assessment report via email
- `config.py`: Added rating categories for consistency

## Usage

1. Start a conversation with the chatbot
2. Complete the basic information steps
3. Answer the technical questions
4. View your assessment in the chat and sidebar
5. Optionally send the assessment report via email

## Future Enhancements

Potential future enhancements include:
- Integration with actual email services (currently mocked)
- More granular skill assessment
- Option to focus on specific areas in the tech stack
- Integration with calendar for scheduling further interviews
- PDF report generation
