# Database Integration for Interview Chatbot

This document explains the database integration that automatically saves all interview data to Supabase PostgreSQL with encryption.

## Overview

After each interview is completed, the system automatically saves:
- **Personal Information** (encrypted): Name, email, phone, location
- **Interview Metadata**: Tech stack, experience level, position, overall rating
- **Questions & Answers** (answers encrypted): All technical questions asked and candidate responses
- **Skill Ratings**: Individual skill scores from AI evaluation

## Database Schema

The system uses 4 main tables:

### 1. `interviews` (Main table)
- `id`: Unique interview identifier
- `email_hash`: SHA256 hash of email for identification
- `overall_rating`: Final hiring recommendation
- `tech_stack`: Technologies the candidate knows
- `experience_years`: Years of experience
- `position`: Position applied for
- `interview_date`: When the interview was conducted
- `status`: Interview status (completed, etc.)

### 2. `candidate_info` (Encrypted personal data)
- `interview_id`: Links to interviews table
- `encrypted_name`: Encrypted full name
- `encrypted_email`: Encrypted email address
- `encrypted_phone`: Encrypted phone number
- `encrypted_location`: Encrypted location

### 3. `questions_answers` (Q&A data)
- `interview_id`: Links to interviews table
- `question_number`: Order of the question
- `question_text`: The technical question asked
- `encrypted_answer`: Encrypted candidate response
- `technology`: Which technology this question relates to

### 4. `skill_ratings` (AI evaluation)
- `interview_id`: Links to interviews table
- `skill_name`: Name of the skill/technology
- `score`: Rating from 1-5
- `max_score`: Maximum possible score (5)

## Setup Instructions

### 1. Create Supabase Project
1. Go to [Supabase](https://supabase.com) and create a new project
2. Wait for the project to be fully initialized

### 2. Create Database Tables
1. Go to your Supabase project dashboard
2. Navigate to **SQL Editor**
3. Copy the SQL from `database/schema.py` (CREATE_TABLES_SQL)
4. Paste and run the SQL to create all tables

### 3. Configure Environment Variables
1. Copy `.env.example` to `.env`
2. Fill in your Supabase credentials:
```bash
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-key-here
```

### 4. Install Dependencies
```bash
pip install supabase python-dotenv
```

### 5. Test the Setup
Run the database test utility:
```bash
python database/test_db.py
```

## Security Features

### Encryption
- **Personal Information**: Names, emails, phone numbers, and locations are encrypted before storage
- **Interview Answers**: All candidate responses are encrypted
- **Email Hashing**: Emails are hashed (SHA256) for identification without storing plaintext
- **Questions**: Technical questions are stored in plaintext (not sensitive)

### Data Privacy
- **GDPR Compliant**: Personal data is encrypted and can be deleted
- **Data Retention**: Configurable retention periods
- **Access Control**: Supabase Row Level Security (RLS) can be configured
- **Audit Trail**: All database operations are logged

## Usage in Code

The database integration is automatically triggered when an interview completes:

```python
from database.models import interview_data_manager

# This happens automatically in complete_interview()
interview_id = interview_data_manager.save_complete_interview(
    candidate_data=candidate_data,
    qa_pairs=qa_pairs,
    ratings=ratings,
    overall_rating=overall_rating
)
```

## Retrieving Data

To retrieve and decrypt interview data:

```python
# Get interview by ID
interview_data = interview_data_manager.get_interview_by_id(interview_id)

# Access decrypted data
candidate_name = interview_data['candidate_info']['name']
qa_pairs = interview_data['qa_pairs']
ratings = interview_data['ratings']
```

## Configuration

Database behavior can be configured in `config.py`:

```python
DATABASE_CONFIG = {
    "save_to_database": True,           # Enable/disable database saving
    "encrypt_sensitive_data": True,     # Enable encryption
    "auto_save_on_completion": True,    # Auto-save when interview completes
    "retention_days": 365               # How long to keep data
}
```

## Error Handling

The system includes comprehensive error handling:
- **Connection Failures**: Graceful fallback, interview continues
- **Save Failures**: User is notified, but interview completes
- **Encryption Errors**: Fallback to base64 encoding
- **Detailed Logging**: All operations are logged for debugging

## Data Export

You can export interview data from Supabase:
1. Go to **Table Editor** in your Supabase dashboard
2. Select the table you want to export
3. Use the **Export** button to download as CSV/JSON

## GDPR Compliance

The system supports GDPR requirements:
- **Right to be Forgotten**: Delete interview records by ID
- **Data Portability**: Export personal data
- **Consent Management**: Can be extended to track consent
- **Data Minimization**: Only necessary data is stored

## Troubleshooting

### Common Issues

1. **"Import supabase could not be resolved"**
   - Run: `pip install supabase`

2. **"Missing Supabase configuration"**
   - Check `.env` file has correct SUPABASE_URL and SUPABASE_KEY

3. **"Database connection test failed"**
   - Verify Supabase project is running
   - Check network connectivity
   - Verify credentials are correct

4. **"Table doesn't exist"**
   - Run the SQL schema in Supabase SQL Editor
   - Check table creation was successful

### Testing

Use the test utility to verify everything works:
```bash
python database/test_db.py
```

This will:
- Test database connection
- Save sample encrypted data
- Retrieve and decrypt the data
- Verify all operations work correctly

## Performance Considerations

- **Indexes**: Automatic indexes on frequently queried fields
- **Batch Operations**: Multiple records saved in single transactions
- **Connection Pooling**: Supabase handles connection management
- **Caching**: Consider adding caching for frequently accessed data

## Monitoring

Monitor your database usage in Supabase:
- **Database Size**: Track storage usage
- **API Requests**: Monitor API call volume
- **Performance**: Check query performance
- **Logs**: Review database logs for issues
