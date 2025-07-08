"""
SQL scripts for creating the required database tables in Supabase PostgreSQL
"""

# Run these SQL commands in your Supabase SQL editor to create the necessary tables

CREATE_TABLES_SQL = """
-- Main interviews table
CREATE TABLE IF NOT EXISTS interviews (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email_hash VARCHAR(64) NOT NULL,
    overall_rating TEXT NOT NULL,
    tech_stack TEXT,
    experience_years TEXT,
    position TEXT,
    interview_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status VARCHAR(20) DEFAULT 'completed',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Encrypted candidate personal information
CREATE TABLE IF NOT EXISTS candidate_info (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    interview_id UUID REFERENCES interviews(id) ON DELETE CASCADE,
    encrypted_name TEXT NOT NULL,
    encrypted_email TEXT NOT NULL,
    encrypted_phone TEXT,
    encrypted_location TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Questions and encrypted answers
CREATE TABLE IF NOT EXISTS questions_answers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    interview_id UUID REFERENCES interviews(id) ON DELETE CASCADE,
    question_number INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    encrypted_answer TEXT NOT NULL,
    technology VARCHAR(100),
    asked_at TIMESTAMPTZ DEFAULT NOW()
);

-- Skill ratings
CREATE TABLE IF NOT EXISTS skill_ratings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    interview_id UUID REFERENCES interviews(id) ON DELETE CASCADE,
    skill_name VARCHAR(100) NOT NULL,
    score INTEGER NOT NULL CHECK (score >= 1 AND score <= 5),
    max_score INTEGER DEFAULT 5,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_interviews_email_hash ON interviews(email_hash);
CREATE INDEX IF NOT EXISTS idx_interviews_date ON interviews(interview_date);
CREATE INDEX IF NOT EXISTS idx_candidate_info_interview_id ON candidate_info(interview_id);
CREATE INDEX IF NOT EXISTS idx_questions_answers_interview_id ON questions_answers(interview_id);
CREATE INDEX IF NOT EXISTS idx_questions_answers_question_number ON questions_answers(interview_id, question_number);
CREATE INDEX IF NOT EXISTS idx_skill_ratings_interview_id ON skill_ratings(interview_id);

-- Row Level Security (RLS) policies - optional but recommended
ALTER TABLE interviews ENABLE ROW LEVEL SECURITY;
ALTER TABLE candidate_info ENABLE ROW LEVEL SECURITY;
ALTER TABLE questions_answers ENABLE ROW LEVEL SECURITY;
ALTER TABLE skill_ratings ENABLE ROW LEVEL SECURITY;

-- Basic policy to allow all operations for authenticated users
-- You may want to customize these based on your specific security requirements
CREATE POLICY "Enable all operations for authenticated users" ON interviews
    FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Enable all operations for authenticated users" ON candidate_info
    FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Enable all operations for authenticated users" ON questions_answers
    FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Enable all operations for authenticated users" ON skill_ratings
    FOR ALL USING (auth.role() = 'authenticated');
"""

# Instructions for setup
SETUP_INSTRUCTIONS = """
To set up the database:

1. Go to your Supabase project dashboard
2. Navigate to the SQL Editor
3. Create a new query and paste the CREATE_TABLES_SQL above
4. Run the query to create all necessary tables and indexes

5. Set up your environment variables in a .env file:
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_KEY=your_supabase_anon_key

6. Make sure your Supabase project has the uuid-ossp extension enabled:
   - Go to Database > Extensions in your Supabase dashboard
   - Enable the "uuid-ossp" extension if not already enabled

The tables created:
- interviews: Main interview records with basic info and overall rating
- candidate_info: Encrypted personal information (name, email, phone, location)
- questions_answers: All technical questions asked and encrypted answers
- skill_ratings: Individual skill scores from the AI evaluation

All sensitive data (personal info and answers) are encrypted before storage.
"""
