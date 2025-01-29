import os
import asyncio
import openai
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
openai_client = OpenAI(api_key=os.getenv('OPENAIAPIKEY'))

def get_chatgpt_response(user_message: str) -> None:
    resp = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_message}]
        )
    return resp.choices[0].message.content