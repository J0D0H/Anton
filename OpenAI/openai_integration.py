import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set the OpenAI API key
openai.api_key = os.getenv('OPENAIAPIKEY')

def get_chatgpt_response(user_message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        return response['choices'][0]['message']['content']  # Return the bot's response
    except Exception as e:
        print(f"Error while fetching from OpenAI: {e}")
        return "Error occurred while fetching the response."