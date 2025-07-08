"""
Configuration for conversation steps and keywords
"""
from validators import (
    validate_name, validate_email, validate_phone, validate_experience,
    validate_position, validate_location, validate_tech_stack
)

# AI Provider Configuration
AI_PROVIDERS = {
    "ollama": {
        "name": "Llama 3.1 8B (Ollama)",
        "model": "llama3.1:8b",
        "enabled": True
    }
}

# Default AI provider
DEFAULT_AI_PROVIDER = "ollama"

# Question steps configuration
STEPS = [
    {
        "question": "What's your full name?",
        "key": "name",
        "validator": validate_name
    },
    {
        "question": "What's your email address?",
        "key": "email", 
        "validator": validate_email
    },
    {
        "question": "What's your phone number?",
        "key": "phone",
        "validator": validate_phone
    },
    {
        "question": "How many years of experience do you have?",
        "key": "experience",
        "validator": validate_experience
    },
    {
        "question": "What position are you interested in?",
        "key": "position",
        "validator": validate_position
    },
    {
        "question": "Where are you currently located?",
        "key": "location",
        "validator": validate_location
    },
    {
        "question": "Please list your tech stack (languages, frameworks, databases, tools).",
        "key": "tech_stack",
        "validator": validate_tech_stack
    }
]

# Conversation-ending keywords
END_KEYWORDS = ["exit", "quit", "bye", "end"]
RETRY_KEYWORDS = ["retry", "try again"]
RESTART_KEYWORDS = ["restart", "start over"]

# Rating categories
HIRE_RATINGS = [
    "Very Strong Hire",
    "Strong Hire",
    "OK Hire",
    "Weak Hire",
    "Bad Hire"
]

# Initial greeting message
INITIAL_GREETING = """Hello! I'm TalentScout's Hiring Assistant. I'll help you with your application by asking a few questions.

Commands you can use:
- Type 'exit' to end the chat
- Type 'retry' to repeat the current question
- Type 'restart' to start from the beginning

Let's get started! What's your full name?"""

# Interview Configuration
QUESTIONS_PER_TECHNOLOGY = 1  # Number of questions to ask per technology in the tech stack

# Security Configuration
SECURITY_CONFIG = {
    "session_timeout_minutes": 30,
    "data_retention_days": 30,
    "enable_encryption": True,
    "enable_gdpr_compliance": True,
    "require_privacy_consent": True,
    "enable_data_masking": True
}

# Privacy and GDPR settings
PRIVACY_CONFIG = {
    "privacy_notice_required": True,
    "data_deletion_schedule_days": 30,
    "anonymize_logs": True,
    "mask_sensitive_data": True
}

# Database Configuration
DATABASE_CONFIG = {
    "save_to_database": True,
    "encrypt_sensitive_data": True,
    "auto_save_on_completion": True,
    "retention_days": 365  # How long to keep interview data
}
