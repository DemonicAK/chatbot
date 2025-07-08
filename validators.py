"""
Validation functions for user input with security enhancements
"""
import re
import logging

logger = logging.getLogger(__name__)

def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent injection attacks"""
    if not isinstance(text, str):
        return str(text)
    
    # Remove potentially harmful characters and patterns
    sanitized = re.sub(r'[<>"\']', '', text)
    sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r'<script.*?</script>', '', sanitized, flags=re.IGNORECASE)
    return sanitized.strip()

def validate_name(name):
    """Validate name - only alphabets, spaces, hyphens, and apostrophes allowed"""
    if not name.strip():
        return False, "Name cannot be empty."
    
    # Sanitize input
    name = sanitize_input(name)
    
    # Enhanced pattern to allow hyphens and apostrophes (for names like O'Connor, Jean-Pierre)
    if not re.match(r"^[a-zA-Z\s\-'\.]{2,50}$", name.strip()):
        return False, "Name should contain only letters, spaces, hyphens, and apostrophes (2-50 characters)."
    
    # Check for reasonable length
    if len(name.strip()) > 50:
        return False, "Name is too long (maximum 50 characters)."
    
    return True, ""

def validate_email(email):
    """Validate email format using enhanced regex"""
    if not email.strip():
        return False, "Email cannot be empty."
    
    # Sanitize input
    email = sanitize_input(email)
    
    # Enhanced email pattern
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_pattern, email.strip()):
        return False, "Please enter a valid email address."
    
    # Additional length checks
    if len(email) > 254:  # RFC 5321 limit
        return False, "Email address is too long."
    
    return True, ""

def validate_phone(phone):
    """Validate phone number - supports various formats"""
    if not phone.strip():
        return False, "Phone number cannot be empty."
    
    # Sanitize input
    phone = sanitize_input(phone)
    
    # Remove all non-digit characters for validation
    phone_digits = re.sub(r'\D', '', phone.strip())
    
    if not phone_digits:
        return False, "Phone number must contain digits."
    
    # Check length (support international numbers)
    if len(phone_digits) < 10 or len(phone_digits) > 15:
        return False, "Phone number should be between 10-15 digits."
    
    # If exactly 10 digits, assume domestic format
    if len(phone_digits) == 10:
        return True, ""
    
    # For international numbers, be more flexible
    return True, ""

def validate_experience(experience):
    """Validate experience with enhanced checks"""
    if not experience.strip():
        return False, "Experience cannot be empty."
    
    # Sanitize input
    experience = sanitize_input(experience)
    
    try:
        exp_num = float(experience.strip())  # Allow decimal years
        if exp_num < 0:
            return False, "Experience cannot be negative."
        if exp_num > 60:  # More reasonable upper limit
            return False, "Experience seems too high. Please enter a realistic number."
        return True, ""
    except ValueError:
        return False, "Experience should be a number (e.g., 2, 3.5, 10)."

def validate_position(position):
    """Validate position input with security enhancements"""
    if not position.strip():
        return False, "Position cannot be empty."
    
    # Sanitize input
    position = sanitize_input(position)
    
    if len(position) < 2:
        return False, "Position must be at least 2 characters long."
    
    if len(position) > 100:
        return False, "Position must be less than 100 characters long."
    
    # Enhanced pattern for position names
    if not re.match(r'^[a-zA-Z0-9\s\-\(\)\.\/\+]+$', position):
        return False, "Position contains invalid characters. Please use only letters, numbers, spaces, hyphens, parentheses, and common symbols."
    
    return True, ""

def validate_location(location):
    """Validate location with security enhancements"""
    if not location.strip():
        return False, "Location cannot be empty."
    
    # Sanitize input
    location = sanitize_input(location)
    
    if len(location) < 2:
        return False, "Location must be at least 2 characters long."
    
    if len(location) > 100:
        return False, "Location must be less than 100 characters long."
    
    # Allow letters, spaces, commas, hyphens, and periods for location names
    if not re.match(r'^[a-zA-Z0-9\s\,\-\.]+$', location):
        return False, "Location contains invalid characters."
    
    return True, ""

def validate_tech_stack(tech_stack):
    """Validate tech stack with security enhancements"""
    if not tech_stack.strip():
        return False, "Tech stack cannot be empty."
    
    # Sanitize input
    tech_stack = sanitize_input(tech_stack)
    
    if len(tech_stack) < 2:
        return False, "Tech stack must be at least 2 characters long."
    
    if len(tech_stack) > 500:
        return False, "Tech stack description is too long (maximum 500 characters)."
    
    # Allow a broader range of characters for tech stack (including +, #, etc.)
    if not re.match(r'^[a-zA-Z0-9\s\,\-\.\+\#\/\(\)]+$', tech_stack):
        return False, "Tech stack contains invalid characters."
    
    return True, ""
