# audio_generation.py

import sys
import os
from openai import OpenAI
from exception import CustomException
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())


# Set up OpenAI API key and AWS credentials
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_audio(question):
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="echo",
            input=question
        )
        print(response)
        return response
    except Exception as e:
        raise CustomException("Error generating audio", error_detail=sys.exc_info())
    