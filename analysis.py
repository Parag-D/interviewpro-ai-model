import os
from question_generation import global_questions
from openai import OpenAI
from dotenv import find_dotenv, load_dotenv
from prompt import analysis_prompt
import base64
import requests
from io import BytesIO

# Load environment variables
load_dotenv(find_dotenv())

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI()

def analyze_interview_with_transcript(video_transcript):
 
    # Generate chat-based completion'
    chat_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": analysis_prompt + global_questions + video_transcript},
            # You can add more user messages if needed
            # {"role": "user", "content": "Candidate's response..."},
        ],
    )

    # Extract and return the content from the response
    return chat_response.choices[0].message.content