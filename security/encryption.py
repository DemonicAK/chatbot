"""
Data encryption utilities for sensitive information
"""
import hashlib
import base64
import os
import logging

logger = logging.getLogger(__name__)

# Try to import cryptography, fallback to base64 if not available
try:
    from cryptography.fernet import Fernet
    ENCRYPTION_AVAILABLE = True
except ImportError:
    logger.warning("Cryptography library not available. Using base64 encoding as fallback.")
    ENCRYPTION_AVAILABLE = False

class DataEncryption:
    """Handle encryption and decryption of sensitive data"""
    
    def __init__(self):
        if ENCRYPTION_AVAILABLE:
            self.key = self._get_or_create_key()
            self.cipher_suite = Fernet(self.key)
        else:
            self.key = None
            self.cipher_suite = None
            logger.warning("Using fallback encryption (base64 encoding)")
    
    def _get_or_create_key(self):
        """Generate or load encryption key"""
        if not ENCRYPTION_AVAILABLE:
            return None
            
        key_file = '.env_key'
        try:
            if os.path.exists(key_file):
                with open(key_file, 'rb') as f:
                    return f.read()
            else:
                key = Fernet.generate_key()
                with open(key_file, 'wb') as f:
                    f.write(key)
                # Add to .gitignore if it exists
                self._add_to_gitignore(key_file)
                return key
        except Exception as e:
            logger.error(f"Error handling encryption key: {e}")
            # Fallback to session-based key (not persistent)
            return Fernet.generate_key()
    
    def _add_to_gitignore(self, filename):
        """Add filename to .gitignore if it exists"""
        try:
            gitignore_path = '.gitignore'
            if os.path.exists(gitignore_path):
                with open(gitignore_path, 'r') as f:
                    content = f.read()
                if filename not in content:
                    with open(gitignore_path, 'a') as f:
                        f.write(f"\n{filename}\n")
        except Exception as e:
            logger.warning(f"Could not update .gitignore: {e}")
    
    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        try:
            if ENCRYPTION_AVAILABLE and self.cipher_suite:
                return self.cipher_suite.encrypt(data.encode()).decode()
            else:
                # Fallback to base64 encoding (not secure, but better than plaintext)
                return base64.b64encode(data.encode()).decode()
        except Exception as e:
            logger.error(f"Encryption error: {e}")
            return data  # Fallback to unencrypted in case of error
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        try:
            if ENCRYPTION_AVAILABLE and self.cipher_suite:
                return self.cipher_suite.decrypt(encrypted_data.encode()).decode()
            else:
                # Fallback from base64 encoding
                return base64.b64decode(encrypted_data.encode()).decode()
        except Exception as e:
            logger.error(f"Decryption error: {e}")
            return encrypted_data  # Fallback to returning as-is
    
    def hash_email(self, email: str) -> str:
        """Hash email for identification without storing plaintext"""
        return hashlib.sha256(email.encode()).hexdigest()
    
    def is_encrypted(self, data: str) -> bool:
        """Check if data appears to be encrypted"""
        try:
            if ENCRYPTION_AVAILABLE and self.cipher_suite:
                # Try to decrypt - if successful, it was encrypted
                self.cipher_suite.decrypt(data.encode())
                return True
            else:
                # For base64, check if it's valid base64
                base64.b64decode(data.encode())
                return True
        except:
            return False
