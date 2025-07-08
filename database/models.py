"""
Database models and operations for interview data storage
"""
import json
import logging
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from security.encryption import DataEncryption
from database.connection import supabase_manager

logger = logging.getLogger(__name__)

class InterviewDataManager:
    """Manage interview data storage in Supabase with encryption"""
    
    def __init__(self):
        self.encryption = DataEncryption()
        self.supabase_manager = supabase_manager
        self.client = None
        
        if self.supabase_manager and self.supabase_manager.is_available():
            self.client = self.supabase_manager.get_client()
    
    def is_available(self) -> bool:
        """Check if database storage is available"""
        return (self.supabase_manager is not None and 
                self.supabase_manager.is_available() and 
                self.client is not None)
    
    def save_complete_interview(self, 
                              candidate_data: Dict[str, Any],
                              qa_pairs: List[Dict[str, str]],
                              ratings: Dict[str, int],
                              overall_rating: str) -> Optional[str]:
        """
        Save complete interview data to Supabase after encryption
        
        Returns: interview_id if successful, None if failed
        """
        if not self.is_available():
            logger.warning("Database not available - skipping save operation")
            return None
            
        try:
            # Create interview record
            interview_id = self._create_interview_record(candidate_data, overall_rating)
            
            if not interview_id:
                logger.error("Failed to create interview record")
                return None
            
            # Save candidate personal info (encrypted)
            self._save_candidate_info(interview_id, candidate_data)
            
            # Save questions and answers
            self._save_questions_answers(interview_id, qa_pairs)
            
            # Save ratings
            self._save_ratings(interview_id, ratings)
            
            logger.info(f"Successfully saved complete interview data with ID: {interview_id}")
            return interview_id
            
        except Exception as e:
            logger.error(f"Error saving interview data: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return None
    
    def _create_interview_record(self, candidate_data: Dict[str, Any], overall_rating: str) -> Optional[str]:
        """Create main interview record"""
        try:
            # Hash email for unique identification without storing plaintext
            email_hash = self.encryption.hash_email(candidate_data.get('email', ''))
            
            interview_data = {
                'email_hash': email_hash,
                'overall_rating': overall_rating,
                'tech_stack': candidate_data.get('tech_stack', ''),
                'experience_years': candidate_data.get('experience', ''),
                'position': candidate_data.get('position', ''),
                'interview_date': datetime.now(timezone.utc).isoformat(),
                'status': 'completed'
            }
            
            result = self.client.table('interviews').insert(interview_data).execute()
            
            if result.data and len(result.data) > 0:
                return result.data[0]['id']
            else:
                logger.error("No data returned from interview insert")
                return None
                
        except Exception as e:
            logger.error(f"Error creating interview record: {e}")
            return None
    
    def _save_candidate_info(self, interview_id: str, candidate_data: Dict[str, Any]) -> bool:
        """Save encrypted candidate personal information"""
        try:
            # Encrypt sensitive personal data
            encrypted_name = self.encryption.encrypt_data(candidate_data.get('name', ''))
            encrypted_email = self.encryption.encrypt_data(candidate_data.get('email', ''))
            encrypted_phone = self.encryption.encrypt_data(candidate_data.get('phone', ''))
            encrypted_location = self.encryption.encrypt_data(candidate_data.get('location', ''))
            
            candidate_info = {
                'interview_id': interview_id,
                'encrypted_name': encrypted_name,
                'encrypted_email': encrypted_email,
                'encrypted_phone': encrypted_phone,
                'encrypted_location': encrypted_location,
                'created_at': datetime.now(timezone.utc).isoformat()
            }
            
            result = self.client.table('candidate_info').insert(candidate_info).execute()
            
            if result.data:
                logger.info(f"Successfully saved encrypted candidate info for interview {interview_id}")
                return True
            else:
                logger.error("Failed to save candidate info")
                return False
                
        except Exception as e:
            logger.error(f"Error saving candidate info: {e}")
            return False
    
    def _save_questions_answers(self, interview_id: str, qa_pairs: List[Dict[str, str]]) -> bool:
        """Save all questions and answers"""
        try:
            qa_records = []
            
            for i, qa_pair in enumerate(qa_pairs):
                question_text = qa_pair.get('question', '')
                answer_text = qa_pair.get('answer', '')
                technology = qa_pair.get('technology', 'general')
                
                # Encrypt the answer (questions are not sensitive)
                encrypted_answer = self.encryption.encrypt_data(answer_text)
                
                qa_record = {
                    'interview_id': interview_id,
                    'question_number': i + 1,
                    'question_text': question_text,
                    'encrypted_answer': encrypted_answer,
                    'technology': technology,
                    'asked_at': datetime.now(timezone.utc).isoformat()
                }
                qa_records.append(qa_record)
            
            if qa_records:
                result = self.client.table('questions_answers').insert(qa_records).execute()
                
                if result.data:
                    logger.info(f"Successfully saved {len(qa_records)} Q&A pairs for interview {interview_id}")
                    return True
                else:
                    logger.error("Failed to save questions and answers")
                    return False
            else:
                logger.warning("No Q&A pairs to save")
                return True
                
        except Exception as e:
            logger.error(f"Error saving questions and answers: {e}")
            return False
    
    def _save_ratings(self, interview_id: str, ratings: Dict[str, int]) -> bool:
        """Save skill ratings"""
        try:
            rating_records = []
            
            for skill, score in ratings.items():
                rating_record = {
                    'interview_id': interview_id,
                    'skill_name': skill,
                    'score': score,
                    'max_score': 5,
                    'created_at': datetime.now(timezone.utc).isoformat()
                }
                rating_records.append(rating_record)
            
            if rating_records:
                result = self.client.table('skill_ratings').insert(rating_records).execute()
                
                if result.data:
                    logger.info(f"Successfully saved {len(rating_records)} skill ratings for interview {interview_id}")
                    return True
                else:
                    logger.error("Failed to save skill ratings")
                    return False
            else:
                logger.warning("No ratings to save")
                return True
                
        except Exception as e:
            logger.error(f"Error saving ratings: {e}")
            return False
    
    def get_interview_by_id(self, interview_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve and decrypt interview data by ID"""
        try:
            # Get main interview data
            interview_result = self.client.table('interviews').select('*').eq('id', interview_id).execute()
            
            if not interview_result.data:
                return None
            
            interview_data = interview_result.data[0]
            
            # Get and decrypt candidate info
            candidate_result = self.client.table('candidate_info').select('*').eq('interview_id', interview_id).execute()
            if candidate_result.data:
                candidate_info = candidate_result.data[0]
                interview_data['candidate_info'] = {
                    'name': self.encryption.decrypt_data(candidate_info['encrypted_name']),
                    'email': self.encryption.decrypt_data(candidate_info['encrypted_email']),
                    'phone': self.encryption.decrypt_data(candidate_info['encrypted_phone']),
                    'location': self.encryption.decrypt_data(candidate_info['encrypted_location'])
                }
            
            # Get questions and answers
            qa_result = self.client.table('questions_answers').select('*').eq('interview_id', interview_id).order('question_number').execute()
            if qa_result.data:
                qa_pairs = []
                for qa in qa_result.data:
                    qa_pairs.append({
                        'question': qa['question_text'],
                        'answer': self.encryption.decrypt_data(qa['encrypted_answer']),
                        'technology': qa['technology']
                    })
                interview_data['qa_pairs'] = qa_pairs
            
            # Get ratings
            ratings_result = self.client.table('skill_ratings').select('*').eq('interview_id', interview_id).execute()
            if ratings_result.data:
                ratings = {}
                for rating in ratings_result.data:
                    ratings[rating['skill_name']] = rating['score']
                interview_data['ratings'] = ratings
            
            return interview_data
            
        except Exception as e:
            logger.error(f"Error retrieving interview data: {e}")
            return None

# Global instance - will be available even if database is not configured
try:
    interview_data_manager = InterviewDataManager()
except Exception as e:
    logger.error(f"Failed to create InterviewDataManager: {e}")
    interview_data_manager = None
