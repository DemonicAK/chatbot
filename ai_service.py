"""
AI integration for generating technical questions
Uses Ollama (Llama 3.1) locally
"""
import streamlit as st
import ollama
import logging
import re
from dotenv import load_dotenv
from config import AI_PROVIDERS, DEFAULT_AI_PROVIDER
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai_service")

# Load environment variables
load_dotenv()

def get_current_ai_provider():
    """Get the currently selected AI provider"""
    return st.session_state.get("ai_provider", DEFAULT_AI_PROVIDER)

def set_ai_provider(provider):
    """Set the AI provider"""
    if provider in AI_PROVIDERS:
        st.session_state["ai_provider"] = provider
        return True
    return False

def check_ollama_connection():
    """Check if Ollama is running and model is available"""
    try:
        # First check if Ollama service is running
        models = ollama.list()
        if not models or 'models' not in models:
            return False, "Ollama service not responding"
        
        # Check available models
        available_models = [model.model for model in models['models']]
        
        # Check for the exact model name
        if 'llama3.2:1B' in available_models:
            return True, "Llama 3.2 1B model available"

        return False, f"Model llama3.2:1B not found. Available: {available_models}"
    except Exception as e:
        return False, f"Connection error: {str(e)}"
def generate_next_question_ollama(tech_stack, experience_level, interested_role, previous_question=None, previous_answer=None, tech_focus=None): 
    """Generate a single follow-up technical interview question using Llama 3.2, based on previous responses."""

    # Enhanced experience to difficulty mapping with specific expectations
    experience_num = int(experience_level.split('-')[0] if '-' in experience_level else experience_level.replace('+', ''))
    if experience_num < 1:
        difficulty_level = "entry-level"
        complexity_desc = "basic concepts, simple implementations, and fundamental understanding"
    elif experience_num < 3:
        difficulty_level = "junior-level"
        complexity_desc = "practical application, debugging skills, and understanding of common patterns"
    elif experience_num < 5:
        difficulty_level = "mid-level"
        complexity_desc = "design decisions, performance considerations, and best practices"
    elif experience_num < 8:
        difficulty_level = "senior-level"
        complexity_desc = "architecture decisions, trade-offs, scalability, and team leadership"
    else:
        difficulty_level = "expert-level"
        complexity_desc = "system design, optimization, mentoring, and industry innovations"

    # Role-specific context mapping
    role_context = get_role_specific_context(interested_role)
    tech_context = get_tech_specific_context(tech_focus)

    # Build the enhanced prompt based on whether this is the first question or a follow-up
    if previous_question and previous_answer:
        # This is a follow-up question
        prompt = f"""
You are a senior technical interviewer at a top tech company, evaluating a {difficulty_level} candidate for the role of **{interested_role}**.

CANDIDATE PROFILE:
- Role: {interested_role} ({role_context['responsibilities']})
- Tech Stack: {tech_stack}
- Experience: {experience_level} years ({difficulty_level})
- Expected Skills: {complexity_desc}

CURRENT FOCUS: {tech_focus}
- Key Areas: {', '.join(tech_context['question_types'])}
- Core Concepts: {', '.join(tech_context['concepts'])}

INTERVIEW CONTEXT:
Previous Question: {previous_question}
Candidate's Answer: {previous_answer}

TASK:
Generate ONE strategic follow-up question that:
1. Builds naturally on their previous answer, showing you listened
2. Probes deeper into {tech_focus} with {difficulty_level} complexity
3. Tests {role_context['key_skills'][0]} and {role_context['key_skills'][1]} specifically
4. Focuses on real-world scenarios a {interested_role} faces daily
5. Evaluates {complexity_desc} appropriate for {experience_level} years experience

REQUIREMENTS:
- Question should test practical problem-solving, not syntax memorization
- Include a realistic scenario or constraint they might encounter
- Make it specific to {role_context['focus_areas'][0]} and {role_context['focus_areas'][1]}
- Difficulty appropriate for someone who should know {complexity_desc}

Return ONLY the interview question - no explanations or introductions."""
    else:
        # This is the first question for this technology
        prompt = f"""
You are a senior technical interviewer at a top tech company, evaluating a {difficulty_level} candidate for the role of **{interested_role}**.

CANDIDATE PROFILE:
- Role: {interested_role} ({role_context['responsibilities']})
- Tech Stack: {tech_stack}
- Experience: {experience_level} years ({difficulty_level})
- Expected Skills: {complexity_desc}

CURRENT FOCUS: {tech_focus}
- Question Types: {', '.join(tech_context['question_types'])}
- Core Concepts: {', '.join(tech_context['concepts'])}
- Role Focus Areas: {', '.join(role_context['focus_areas'][:3])}

TASK:
Generate ONE strategic opening question about {tech_focus} that:
1. Tests {difficulty_level} knowledge appropriate for {experience_level} years experience
2. Focuses on {role_context['focus_areas'][0]} - a core responsibility for {interested_role}
3. Includes a realistic scenario they'd encounter in this role
4. Evaluates {complexity_desc}
5. Tests both theoretical understanding AND practical application

REQUIREMENTS:
- Make it specific to {tech_focus} and relevant to {interested_role} work
- Include a real-world context or constraint
- Test problem-solving approach, not just memorized facts
- Appropriate difficulty for someone expected to handle {complexity_desc}
- Should reveal their depth of experience with {tech_focus}

Return ONLY the interview question - no explanations or introductions."""

    try:
        response = ollama.chat(
            model='llama3.2:1B',
            messages=[
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            options={
                'temperature': 0.6,
                'top_p': 0.85,
                'num_predict': 200
            }
        )
        logger.info(f"Response from Ollama: {response['message']['content'][:100]}...")
        content = response['message']['content'].strip()
        
        # Clean and validate the question
        question = clean_and_validate_question(content, tech_focus, interested_role, experience_level)
        
        return question
    except Exception as e:
        logger.error(f"Ollama Error: {str(e)}")
        fallback_question = f"How would you solve a typical {tech_focus or 'programming'} challenge in {interested_role} work?"
        return clean_and_validate_question(fallback_question, tech_focus, interested_role, experience_level)


def generate_next_question(tech_stack, tech_focus=None, previous_question=None, previous_answer=None):
    """Generate the next technical question based on tech stack and previous Q&A"""
    experience_level = st.session_state["candidate_data"].get("experience", "3-5")
    role = st.session_state["candidate_data"].get("position", ["Software Engineer"])[0]
    
    logger.info(f"Generating next question for tech_focus: '{tech_focus}' with previous Q&A")
    
    result = generate_next_question_ollama(
        tech_stack, 
        experience_level, 
        role, 
        previous_question, 
        previous_answer, 
        tech_focus
    )
    
    return result

def parse_questions(raw_questions):
    """Parse raw response into a clean list of questions (1 per line, no numbering expected)."""
    # lines = raw_questions.strip().split('\n')
    # questions = [line.strip() for line in lines if line.strip()]
    return raw_questions  # Ensure only 4 questions are returned

def rate_candidate_responses(tech_stack, qa_pairs, interested_role, experience_level):
    """
    Rate a candidate's responses to interview questions using enhanced evaluation criteria.
    """
    try:
        tech_list = [tech.strip() for tech in tech_stack.split(',') if tech.strip()]
        role = interested_role or "Not specified"
        experience = experience_level or "Not specified"
        
        # Get role context for evaluation
        role_context = get_role_specific_context(role)
        
        # Map experience to expected competencies
        experience_num = int(experience.split('-')[0] if '-' in experience else experience.replace('+', ''))
        if experience_num < 1:
            expected_level = "basic understanding and eagerness to learn"
        elif experience_num < 3:
            expected_level = "practical application and debugging skills"
        elif experience_num < 5:
            expected_level = "design decisions and best practices knowledge"
        elif experience_num < 8:
            expected_level = "architectural thinking and leadership capabilities"
        else:
            expected_level = "expert-level insights and innovation"
        
        # Compose enhanced evaluation prompt
        prompt = f"""
You are a Principal Engineer and hiring manager at a top tech company, evaluating a {experience} years experienced candidate for **{role}**.

ROLE CONTEXT:
- Position: {role}
- Responsibilities: {role_context['responsibilities']}
- Key Skills Required: {', '.join(role_context['key_skills'])}
- Focus Areas: {', '.join(role_context['focus_areas'])}

CANDIDATE PROFILE:
- Tech Stack: {tech_stack}
- Experience Level: {experience} years
- Expected Competency: {expected_level}

INTERVIEW RESPONSES:
"""
        for i, pair in enumerate(qa_pairs):
            question = pair['question']
            tech_focus = "General"
            
            # Extract technology focus from question if available
            if question.startswith('[') and ']' in question:
                tech_focus = question.split(']')[0].strip('[')
                question = question.split(']', 1)[1].strip()
            
            prompt += f"\nQ{i+1} ({tech_focus}): {question}\n"
            prompt += f"Answer: {pair['answer']}\n"

        prompt += f"""

EVALUATION TASK:

Rate each technology in their stack using this {experience}-year experience rubric:

FOR {experience} YEARS EXPERIENCE:
- 1 = Poor: Below expectations for {experience} years, lacks fundamental understanding
- 2 = Basic: Meets minimum expectations, surface-level knowledge appropriate for junior level
- 3 = Moderate: Meets expectations for {experience} years, can handle typical {role} tasks
- 4 = Good: Exceeds expectations, shows strong {role} skills and {expected_level}
- 5 = Excellent: Far exceeds expectations, demonstrates expertise beyond {experience} years

EVALUATION CRITERIA:
✓ Technical depth appropriate for {experience} years in {role}
✓ Problem-solving approach and reasoning quality
✓ Understanding of {role_context['focus_areas'][0]} and {role_context['focus_areas'][1]}
✓ Practical experience vs theoretical knowledge
✓ Communication clarity and structured thinking
✓ Awareness of best practices and trade-offs

OVERALL HIRING DECISION:
- Very Strong Hire: Exceptional candidate, hire immediately
- Strong Hire: Great candidate, strong recommendation to hire  
- OK Hire: Adequate candidate, meets bar but not exceptional
- Weak Hire: Below hiring bar, significant concerns
- Bad Hire: Do not hire, major gaps or red flags

FORMAT YOUR RESPONSE EXACTLY AS:

RATINGS:
[Technology1]: [1-5 score]
[Technology2]: [1-5 score]
...

OVERALL: [One of the 5 hiring decisions above]

Evaluate based on answers quality, not just keywords. Consider their {experience} years experience level."""

        # Call Llama 3.1 once — fast, focused
        response = ollama.chat(
            model='llama3.2:1B',
            messages=[
                {
                    'role': 'system',
                    'content': 'You are an experienced technical hiring manager. Score answers based purely on technical merit and problem-solving skill.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            options={
                'temperature': 0.3,
                'top_p': 0.9,
                'num_predict': 1000
            }
        )

        content = response['message']['content'].strip()
        return parse_rating_response(content)

    except Exception as e:
        logger.error(f"Error in rating process: {str(e)}")
        return {"ratings": {}, "overall": "Error in rating process"}
    
def parse_rating_response(response_text):
    """Parse the model's response into a dictionary with tech ratings and overall recommendation."""
    lines = response_text.strip().splitlines()
    ratings = {}
    overall = "Unknown"

    in_ratings_section = False
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.upper().startswith("RATINGS"):
            in_ratings_section = True
            continue
            
        if line.upper().startswith("OVERALL"):
            in_ratings_section = False
            overall_parts = line.split(":", 1)
            if len(overall_parts) > 1:
                overall = overall_parts[1].strip()
            continue
            
        if in_ratings_section and ":" in line:
            tech, score = line.split(":", 1)
            # Extract number from score (handle cases with text)
            import re
            score_digits = re.findall(r'\d+', score.strip())
            if score_digits:
                try:
                    ratings[tech.strip()] = int(score_digits[0])
                except ValueError:
                    continue

    # Return a structured result
    return {
        "ratings": ratings,
        "overall": overall
    }

def get_ai_status():
    """Get status of Ollama"""
    status = {}
    
    # Check Ollama only
    ollama_available, ollama_info = check_ollama_connection()
    status["ollama"] = {
        "available": ollama_available,
        "message": ollama_info
    }
    
    return status

def get_role_specific_context(role):
    """Get role-specific context and expectations for question generation"""
    role_lower = role.lower()
    
    if "frontend" in role_lower or "front-end" in role_lower or "ui" in role_lower:
        return {
            "focus_areas": ["user experience", "performance optimization", "accessibility", "responsive design", "browser compatibility"],
            "responsibilities": "building user interfaces, optimizing user experience, and ensuring cross-browser compatibility",
            "key_skills": ["component architecture", "state management", "performance optimization", "testing"]
        }
    elif "backend" in role_lower or "back-end" in role_lower or "server" in role_lower:
        return {
            "focus_areas": ["API design", "database optimization", "security", "scalability", "microservices"],
            "responsibilities": "designing APIs, managing databases, ensuring security, and building scalable systems",
            "key_skills": ["system architecture", "database design", "security implementation", "performance optimization"]
        }
    elif "fullstack" in role_lower or "full-stack" in role_lower or "full stack" in role_lower:
        return {
            "focus_areas": ["end-to-end development", "API integration", "database design", "user experience"],
            "responsibilities": "developing complete applications from frontend to backend, integrating systems",
            "key_skills": ["full-stack architecture", "API design", "database management", "deployment"]
        }
    elif "devops" in role_lower or "sre" in role_lower or "infrastructure" in role_lower:
        return {
            "focus_areas": ["CI/CD", "containerization", "monitoring", "infrastructure as code", "reliability"],
            "responsibilities": "automating deployments, managing infrastructure, ensuring system reliability",
            "key_skills": ["automation", "monitoring", "containerization", "cloud platforms"]
        }
    elif "data" in role_lower or "analytics" in role_lower or "scientist" in role_lower:
        return {
            "focus_areas": ["data processing", "machine learning", "statistical analysis", "data visualization"],
            "responsibilities": "analyzing data, building ML models, creating insights from data",
            "key_skills": ["data analysis", "machine learning", "statistical modeling", "data visualization"]
        }
    elif "mobile" in role_lower or "ios" in role_lower or "android" in role_lower:
        return {
            "focus_areas": ["mobile UX", "platform-specific features", "performance", "offline functionality"],
            "responsibilities": "developing mobile applications, optimizing for mobile platforms",
            "key_skills": ["platform development", "mobile UI/UX", "performance optimization", "platform integration"]
        }
    else:
        return {
            "focus_areas": ["software design", "problem solving", "code quality", "collaboration"],
            "responsibilities": "developing software solutions, writing maintainable code, collaborating with teams",
            "key_skills": ["programming", "problem solving", "code quality", "teamwork"]
        }

def get_tech_specific_context(tech_focus):
    """Get technology-specific context for targeted question generation"""
    if not tech_focus:
        return {"question_types": ["general problem solving", "code design"], "concepts": ["software engineering principles"]}
    
    tech_lower = tech_focus.lower()
    
    # Programming Languages
    if tech_lower in ["python", "java", "javascript", "typescript", "c++", "c#", "go", "rust"]:
        return {
            "question_types": ["language-specific features", "performance optimization", "design patterns", "best practices"],
            "concepts": [f"{tech_focus} specific features", "memory management", "concurrency", "error handling"]
        }
    
    # Frontend Technologies
    elif tech_lower in ["react", "vue", "angular", "svelte", "nextjs", "nuxt"]:
        return {
            "question_types": ["component design", "state management", "performance", "testing"],
            "concepts": ["component lifecycle", "state management", "virtual DOM", "rendering optimization"]
        }
    
    # Backend Technologies
    elif tech_lower in ["nodejs", "express", "django", "flask", "spring", "fastapi"]:
        return {
            "question_types": ["API design", "middleware", "authentication", "performance"],
            "concepts": ["request handling", "middleware architecture", "security", "scalability"]
        }
    
    # Databases
    elif tech_lower in ["postgresql", "mysql", "mongodb", "redis", "elasticsearch"]:
        return {
            "question_types": ["query optimization", "schema design", "indexing", "performance"],
            "concepts": ["database design", "query optimization", "indexing strategies", "data consistency"]
        }
    
    # Cloud/DevOps
    elif tech_lower in ["aws", "azure", "gcp", "docker", "kubernetes", "terraform"]:
        return {
            "question_types": ["infrastructure design", "deployment strategies", "monitoring", "security"],
            "concepts": ["cloud architecture", "containerization", "infrastructure as code", "scalability"]
        }
    
    else:
        return {
            "question_types": ["implementation", "best practices", "problem solving"],
            "concepts": [f"{tech_focus} fundamentals", "practical application"]
        }

def clean_and_validate_question(question, tech_focus, role, experience_level):
    """Clean and validate the generated question to ensure quality"""
    if not question or len(question.strip()) == 0:
        return f"Can you explain a key concept in {tech_focus} relevant to {role} work?"
    
    # Clean up the question
    question = question.strip()
    
    # Remove common unwanted prefixes/suffixes
    prefixes_to_remove = [
        "Here's a question:", "Question:", "Here's an interview question:",
        "Technical question:", "Interview question:", "Q:", "A good question would be:"
    ]
    
    for prefix in prefixes_to_remove:
        if question.lower().startswith(prefix.lower()):
            question = question[len(prefix):].strip()
    
    # Remove numbering
    question = re.sub(r'^\d+[\.\)]\s*', '', question)
    question = re.sub(r'^[-•*]\s*', '', question)
    
    # Ensure it ends with a question mark
    if not question.endswith('?'):
        question += '?'
    
    # Ensure it's not too long (reasonable interview question length)
    if len(question) > 500:
        question = question[:497] + "...?"
    
    # Ensure it's not too short (should be meaningful)
    if len(question) < 20:
        return f"How would you approach solving a common {tech_focus} challenge in {role} development?"
    
    return question
