"""
Test security features integration
"""
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from security.encryption import DataEncryption
from security.data_privacy import DataPrivacyManager
from security.gdpr_compliance import GDPRCompliance
from validators import sanitize_input, validate_email, validate_name, validate_phone

def test_encryption():
    """Test encryption functionality"""
    print("Testing encryption...")
    
    encryption = DataEncryption()
    test_data = "john.doe@example.com"
    
    # Test encryption/decryption
    encrypted = encryption.encrypt_data(test_data)
    decrypted = encryption.decrypt_data(encrypted)
    
    print(f"Original: {test_data}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Encryption working: {test_data == decrypted}")
    
    # Test email hashing
    email_hash = encryption.hash_email(test_data)
    print(f"Email hash: {email_hash}")
    print()

def test_data_privacy():
    """Test data privacy features"""
    print("Testing data privacy...")
    
    # Test masking
    email = "john.doe@example.com"
    phone = "1234567890"
    name = "John Doe"
    
    masked_email = DataPrivacyManager.mask_email(email)
    masked_phone = DataPrivacyManager.mask_phone_number(phone)
    masked_name = DataPrivacyManager.mask_name(name)
    
    print(f"Original email: {email} -> Masked: {masked_email}")
    print(f"Original phone: {phone} -> Masked: {masked_phone}")
    print(f"Original name: {name} -> Masked: {masked_name}")
    
    # Test anonymization
    data = {"name": name, "email": email, "phone": phone}
    anonymized = DataPrivacyManager.anonymize_for_logging(data)
    print(f"Anonymized data: {anonymized}")
    print()

def test_validators():
    """Test enhanced validators"""
    print("Testing enhanced validators...")
    
    # Test input sanitization
    malicious_input = "<script>alert('xss')</script>John"
    sanitized = sanitize_input(malicious_input)
    print(f"Malicious input: {malicious_input}")
    print(f"Sanitized: {sanitized}")
    
    # Test validators
    test_cases = [
        ("john.doe@example.com", validate_email),
        ("John O'Connor", validate_name),
        ("1234567890", validate_phone),
    ]
    
    for value, validator in test_cases:
        is_valid, message = validator(value)
        print(f"{validator.__name__}('{value}'): {is_valid} - {message}")
    
    print()

def test_integration():
    """Test that all components work together"""
    print("Testing integration...")
    
    # Simulate candidate data
    candidate_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "1234567890",
        "experience": "5",
        "position": "Software Engineer",
        "location": "New York, NY",
        "tech_stack": "Python, JavaScript, React"
    }
    
    # Test encryption of sensitive data
    encryption = DataEncryption()
    sensitive_fields = ["name", "email", "phone"]
    
    encrypted_data = {}
    for key, value in candidate_data.items():
        if key in sensitive_fields:
            encrypted_data[key] = encryption.encrypt_data(value)
        else:
            encrypted_data[key] = value
    
    print("Encrypted sensitive data:")
    for key, value in encrypted_data.items():
        if key in sensitive_fields:
            decrypted = encryption.decrypt_data(value)
            print(f"  {key}: {value[:20]}... (decrypts to: {decrypted})")
        else:
            print(f"  {key}: {value}")
    
    # Test anonymization
    anonymized = DataPrivacyManager.anonymize_for_logging(candidate_data)
    print(f"\nAnonymized for logging: {anonymized}")
    
    print("\nIntegration test complete!")

if __name__ == "__main__":
    print("=== Security Features Test ===\n")
    
    try:
        test_encryption()
        test_data_privacy()
        test_validators()
        test_integration()
        
        print("✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
