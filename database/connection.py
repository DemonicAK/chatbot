"""
Supabase database connection and configuration
"""
import os
import logging
from typing import Optional
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class SupabaseManager:
    """Handle Supabase database connections and operations"""
    
    def __init__(self):
        self.client: Optional[Client] = None
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.connected = False
        
        if not self.url or not self.key:
            logger.warning("Supabase URL or KEY not found in environment variables. Database features will be disabled.")
            return
        
        try:
            self._connect()
        except Exception as e:
            logger.error(f"Failed to initialize Supabase connection: {e}")
    
    def _connect(self):
        """Establish connection to Supabase"""
        try:
            if not self.url or not self.key:
                return False
            self.client = create_client(self.url, self.key)
            self.connected = True
            logger.info("Successfully connected to Supabase")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Supabase: {e}")
            self.connected = False
            return False
    
    def get_client(self) -> Optional[Client]:
        """Get the Supabase client"""
        if not self.connected and self.url and self.key:
            self._connect()
        return self.client if self.connected else None
    
    def is_available(self) -> bool:
        """Check if Supabase is available and configured"""
        return self.connected and self.client is not None
    
    def test_connection(self) -> bool:
        """Test the database connection"""
        try:
            if not self.is_available():
                return False
            # Try a simple query to test connection
            result = self.client.table('interviews').select('id').limit(1).execute()
            return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False

# Global instance - will not raise error if env vars missing
try:
    supabase_manager = SupabaseManager()
except Exception as e:
    logger.error(f"Failed to create SupabaseManager: {e}")
    supabase_manager = None
