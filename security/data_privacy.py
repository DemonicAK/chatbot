"""
Data privacy management utilities
"""
import re
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class DataPrivacyManager:
    """Handle data masking, anonymization, and privacy controls"""
    
    @staticmethod
    def mask_phone_number(phone: str) -> str:
        """Mask phone number: 1234567890 -> 123****890"""
        if len(phone) > 6:
            return phone[:3] + '*' * (len(phone) - 6) + phone[-3:]
        return phone
    
    @staticmethod
    def mask_email(email: str) -> str:
        """Mask email: john@example.com -> j***@example.com"""
        if '@' in email:
            local, domain = email.split('@', 1)
            if len(local) > 1:
                masked_local = local[0] + '*' * (len(local) - 1)
            else:
                masked_local = '*'
            return f"{masked_local}@{domain}"
        return email
    
    @staticmethod
    def mask_name(name: str) -> str:
        """Mask name: John Doe -> J*** D***"""
        parts = name.split()
        masked_parts = []
        for part in parts:
            if len(part) > 1:
                masked_parts.append(part[0] + '*' * (len(part) - 1))
            else:
                masked_parts.append('*')
        return ' '.join(masked_parts)
    
    @staticmethod
    def anonymize_for_logging(data: Dict[str, Any]) -> Dict[str, Any]:
        """Create anonymized version for logging"""
        anonymized = data.copy()
        
        # Mask sensitive fields
        if 'email' in anonymized:
            anonymized['email'] = DataPrivacyManager.mask_email(str(anonymized['email']))
        if 'phone' in anonymized:
            anonymized['phone'] = DataPrivacyManager.mask_phone_number(str(anonymized['phone']))
        if 'name' in anonymized:
            anonymized['name'] = DataPrivacyManager.mask_name(str(anonymized['name']))
        
        return anonymized
    
    @staticmethod
    def is_sensitive_field(field_name: str) -> bool:
        """Check if a field contains sensitive information"""
        sensitive_fields = {'name', 'email', 'phone', 'address', 'location'}
        return field_name.lower() in sensitive_fields
    
    @staticmethod
    def sanitize_for_storage(data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize data for secure storage"""
        sanitized = {}
        for key, value in data.items():
            if isinstance(value, str):
                # Remove potential script injection
                sanitized[key] = re.sub(r'<script.*?</script>', '', str(value), flags=re.IGNORECASE)
                # Remove HTML tags
                sanitized[key] = re.sub(r'<[^>]+>', '', sanitized[key])
            else:
                sanitized[key] = value
        return sanitized
