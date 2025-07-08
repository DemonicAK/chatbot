"""
Database utility script for testing and management
"""
import sys
import os
import logging
from datetime import datetime

# Add the parent directory to Python path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import supabase_manager
from database.models import interview_data_manager
from database.schema import CREATE_TABLES_SQL, SETUP_INSTRUCTIONS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_database_connection():
    """Test the database connection"""
    try:
        print("🔌 Testing database connection...")
        success = supabase_manager.test_connection()
        if success:
            print("✅ Database connection successful!")
            return True
        else:
            print("❌ Database connection failed!")
            return False
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def print_schema_instructions():
    """Print database setup instructions"""
    print("\n" + "="*60)
    print("DATABASE SETUP INSTRUCTIONS")
    print("="*60)
    print(SETUP_INSTRUCTIONS)
    print("\n" + "="*60)
    print("SQL SCHEMA TO RUN IN SUPABASE:")
    print("="*60)
    print(CREATE_TABLES_SQL)

def test_save_sample_data():
    """Test saving sample interview data"""
    try:
        print("\n🧪 Testing sample data save...")
        
        # Sample candidate data
        candidate_data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '+1-555-0123',
            'experience': '5',
            'position': 'Senior Software Engineer',
            'location': 'San Francisco, CA',
            'tech_stack': 'Python, React, PostgreSQL, Docker'
        }
        
        # Sample Q&A pairs
        qa_pairs = [
            {
                'question': 'Explain the difference between list and tuple in Python',
                'answer': 'Lists are mutable while tuples are immutable. Lists use square brackets and tuples use parentheses.',
                'technology': 'Python'
            },
            {
                'question': 'What is a React hook?',
                'answer': 'Hooks are functions that let you use state and other React features in functional components.',
                'technology': 'React'
            },
            {
                'question': 'Explain ACID properties in databases',
                'answer': 'ACID stands for Atomicity, Consistency, Isolation, and Durability - properties that guarantee database transactions are processed reliably.',
                'technology': 'PostgreSQL'
            }
        ]
        
        # Sample ratings
        ratings = {
            'Python': 4,
            'React': 3,
            'PostgreSQL': 4,
            'Docker': 3
        }
        
        overall_rating = "Strong Hire"
        
        # Save to database
        interview_id = interview_data_manager.save_complete_interview(
            candidate_data=candidate_data,
            qa_pairs=qa_pairs,
            ratings=ratings,
            overall_rating=overall_rating
        )
        
        if interview_id:
            print(f"✅ Successfully saved test data with interview ID: {interview_id}")
            
            # Test retrieval
            print("🔍 Testing data retrieval...")
            retrieved_data = interview_data_manager.get_interview_by_id(interview_id)
            
            if retrieved_data:
                print("✅ Successfully retrieved and decrypted interview data!")
                print(f"   - Candidate: {retrieved_data.get('candidate_info', {}).get('name', 'N/A')}")
                print(f"   - Email: {retrieved_data.get('candidate_info', {}).get('email', 'N/A')}")
                print(f"   - Overall Rating: {retrieved_data.get('overall_rating', 'N/A')}")
                qa_pairs = retrieved_data.get('qa_pairs') or []
                print(f"   - Q&A Pairs: {len(qa_pairs)}")
                ratings = retrieved_data.get('ratings') or {}
                print(f"   - Skill Ratings: {len(ratings)}")
            else:
                print("❌ Failed to retrieve interview data")
                
        else:
            print("❌ Failed to save test data")
            
    except Exception as e:
        print(f"❌ Error testing sample data: {e}")
        import traceback
        print(traceback.format_exc())

def main():
    """Main function to run database tests"""
    print("🚀 Interview Database Utility")
    print("="*40)
    
    # Check if environment variables are set
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        print("⚠️  Environment variables not found!")
        print("Please copy .env.example to .env and add your Supabase credentials.")
        print_schema_instructions()
        return
    
    print(f"📍 Supabase URL: {supabase_url}")
    print(f"🔑 Supabase Key: {supabase_key[:20]}...")
    
    # Test connection
    if test_database_connection():
        # Test data operations
        test_save_sample_data()
    else:
        print("\n❌ Cannot proceed with tests due to connection failure.")
        print("Please check your Supabase credentials and ensure the database tables are created.")
        print_schema_instructions()

if __name__ == "__main__":
    main()
