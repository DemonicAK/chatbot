import os
from openai import OpenAI
# import 
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
def generate_questions(tech_stack):
    prompt = f"Generate 3-5 technical interview questions for each of the following technologies: {tech_stack}. Format as a numbered list."
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a technical interviewer."},
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Sorry, I couldn't generate questions at this time. Please make sure your OpenAI API key is set correctly. Error: {str(e)},api-key current: {os.getenv('OPENAI_API_KEY')}"

if True:
    print(f"Using OpenAI API key: {os.getenv('OPENAI_API_KEY')}")
    print("OpenAI client initialized successfully.")
    tech_stack = "Python, JavaScript, SQL"
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    questions = generate_questions(tech_stack)
    print("Generated Questions:")
    print(questions)
    
else:
    print("Failed to initialize OpenAI client. Please check your API key.")