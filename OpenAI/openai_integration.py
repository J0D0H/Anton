from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
openai_client = OpenAI(api_key=os.getenv('OPENAIAPIKEY'))

def get_chatgpt_response(user_message: str) -> str:
    try:
        resp = openai_client.chat.completions.create(
            model="gpt-4o-mini",  # Ensure you're using the correct model
            messages=[{"role": "user", "content": user_message}]
        )
        response = resp.choices[0].message.content
        return response  # Return the generated response
    except Exception as e:
        print(f"Error while fetching from OpenAI: {e}")
        return "Sorry, I couldn't process your request."  # Fallback response