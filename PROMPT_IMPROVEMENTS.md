# AI Service Prompt Improvements

## Overview
The AI service prompts have been significantly enhanced to generate higher quality technical interview questions that are properly aligned with:
- Specific tech stacks and technologies
- Target roles and responsibilities  
- Experience levels and expectations
- Industry standards and real-world scenarios

## Key Improvements Made

### 1. Enhanced Experience Level Mapping
- **Before**: Simple difficulty levels (entry, junior, mid, senior, expert)
- **After**: Detailed competency expectations for each level:
  - Entry-level (< 1 year): Basic concepts, simple implementations, fundamental understanding
  - Junior-level (1-3 years): Practical application, debugging skills, common patterns
  - Mid-level (3-5 years): Design decisions, performance considerations, best practices
  - Senior-level (5-8 years): Architecture decisions, trade-offs, scalability, leadership
  - Expert-level (8+ years): System design, optimization, mentoring, industry innovations

### 2. Role-Specific Context Integration
Added `get_role_specific_context()` function that provides:
- **Focus Areas**: Key technical areas relevant to each role
- **Responsibilities**: Core job functions for context
- **Key Skills**: Essential competencies to evaluate

**Supported Roles**:
- Frontend Developer: UX, performance, accessibility, responsive design
- Backend Developer: API design, databases, security, scalability
- Full Stack Developer: End-to-end development, system integration
- DevOps Engineer: CI/CD, containerization, infrastructure, monitoring
- Data Scientist: Data processing, ML, analytics, visualization
- Mobile Developer: Platform-specific features, mobile UX, performance
- Software Engineer: General software design and best practices

### 3. Technology-Specific Question Types
Added `get_tech_specific_context()` function that tailors questions based on:
- **Programming Languages**: Language features, patterns, performance
- **Frontend Frameworks**: Component design, state management, rendering
- **Backend Technologies**: API design, middleware, authentication
- **Databases**: Query optimization, schema design, indexing
- **Cloud/DevOps**: Infrastructure design, deployment strategies

### 4. Improved Prompt Engineering

#### For Initial Questions:
- Clear role and experience context
- Technology-specific focus areas
- Real-world scenario integration
- Appropriate difficulty calibration
- Emphasis on problem-solving over syntax

#### For Follow-up Questions:
- Builds naturally on previous answers
- Introduces new technical challenges
- Maintains focus on target technology
- Tests progressive skill depth
- Evaluates practical application

### 5. Question Quality Assurance
Added `clean_and_validate_question()` function that:
- Removes unwanted prefixes and formatting
- Ensures proper question format
- Validates appropriate length
- Provides fallbacks for edge cases
- Maintains professional interview tone

### 6. Enhanced Evaluation Criteria
Improved rating prompts with:
- Experience-relative scoring rubrics
- Role-specific evaluation criteria
- Focus on problem-solving approach
- Communication and reasoning assessment
- Industry-standard expectations

## Example Improvements

### Before:
```
"Generate a technical question about React for a 3-5 year candidate."
```

### After:
```
"You are evaluating a mid-level Frontend Developer with 3-5 years experience.
Focus on component design and state management for React.
Test their understanding of performance optimization and user experience.
Include a realistic scenario they'd encounter building user interfaces.
Evaluate design decisions and best practices knowledge."
```

## Benefits

1. **Higher Quality Questions**: More relevant, realistic, and appropriately challenging
2. **Better Role Alignment**: Questions match actual job responsibilities
3. **Experience Calibration**: Difficulty properly scaled to candidate level
4. **Technology Focus**: Deep, specific evaluation of tech stack skills
5. **Real-world Relevance**: Scenarios candidates will actually face
6. **Consistent Evaluation**: Standardized criteria across all assessments

## Usage

The improvements are automatically applied when generating questions through:
- `generate_next_question_ollama()` - Main question generation
- `rate_candidate_responses()` - Enhanced evaluation
- `clean_and_validate_question()` - Quality assurance

No changes needed to existing application code - all improvements are internal to the AI service.
