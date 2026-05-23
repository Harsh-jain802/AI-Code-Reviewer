from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# This is set up for your Groq Key (gsk_...)
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def analyze_code(diff_text):
    prompt = f"""
    You are a Senior Software Engineer. Review these code changes:
    {diff_text}
    
    List:
    1. Potential Bugs
    2. Security Risks
    
    Keep it short and professional.
    """
    
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content