from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
openai_client = OpenAI(api_key=os.getenv('OPENAIAPIKEY'))

async def get_chatgpt_response(user_message: str) -> str:
    try:
        print("Making API request...")
        response = await asyncio.to_thread(openai.ChatCompletion.create,  # This runs the blocking OpenAI request in a separate thread
            model="gpt-4",  # Ensure you're using the correct model
            messages=[{"role": "user", "content": user_message}]
        )
        print("Received response from OpenAI.")
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error while fetching from OpenAI: {e}")
        return "Sorry, I couldn't process your request."  # Fallback response