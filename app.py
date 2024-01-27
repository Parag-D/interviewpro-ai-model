# app.py
import requests
from flask import Flask, request, jsonify
import aiohttp
import os
import json
import asyncio
from openai import AsyncOpenAI
from dotenv import find_dotenv, load_dotenv
from exception import CustomException
from logger import create_logs, log_error
from audio_generation import generate_audio
from question_generation import generate_question_and_audio_async
from video_processing import split_video, download_video_from_s3, generate_video_transcript_from_chunks
from s3_operations import upload_to_s3
import boto3 
from flask_cors import CORS
import re
from analysis import analyze_interview_with_transcript

# Load environment variables
load_dotenv(find_dotenv())

# Set up logging
logger = create_logs()

# Set up OpenAI API key and AWS credentials
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
BACKEND_URL = os.getenv("BACKEND_URL")

# Use AsyncOpenAI for asynchronous calls
client = AsyncOpenAI(api_key=OPENAI_API_KEY)
s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION)

app = Flask(__name__)

CORS(app, origins=['*'])



@app.route('/generate_question_and_audio', methods=['POST'])
async def generate_question_and_audio():
    
    try:
        # Get JSON data from the request body
        request_data = request.get_json()
        print("request data is: ",request_data)
        type(request_data)

        # Extract the 'content' key from the JSON data
        content = request_data.get('content')
        print("content is: ",content)
        type(request_data)

        # Check if 'content' is present in the request data
        if content is None:
            raise ValueError("Invalid request format. 'content' key is missing.")

        # Extract the resume from the JSON data
        resume = content        

        # Call OpenAI API for question generation asynchronously
        cleaned_questions, question_list = generate_question_and_audio_async(resume)

        # Call OpenAI API for audio generation asynchronously
        tasks = [generate_audio(cleaned_question) for cleaned_question in cleaned_questions]
        audio_responses = tasks

        print(audio_responses)

        # Call OpenAI API for audio generation and upload to S3 asynchronously
        tasks = [print(f"Audio for question '{question}' generated") or upload_to_s3(question, response.content) for question, response in zip(question_list, audio_responses)]

        print(tasks)
        # tasks = [upload_to_s3(question, response.content) for question, response in zip(question_list, audio_responses)]
        audio_urls =  tasks

        # Structure responseObj
        responseObj = [
            {"title": question, "audio_url": audio_url}
            for question, audio_url in zip(question_list, audio_urls)
        ]

        print("responseObj is ", responseObj)

        # Structure responseObj

        # Return the generated questions and audio file S3 URLs as a JSON response
        response_data = {
            "responseObj": responseObj
        }

        print("data", response_data)

        logger.info("Successfully generated questions and audio.")

        # # Perform POST request to the specified URL with the generated data
        # url = f"{BACKEND_URL}/"
        # async with aiohttp.ClientSession() as session:
        #     async with session.post(url, json=response_data) as post_req:
        #         post_req_text = await post_req.text()


        # Perform POST request to the specified URL with the generated data
        url = f"{BACKEND_URL}/"
        response = requests.post(url, json=response_data)

        # Access the response text
        post_req_text = response.text

        logger.info("Successfully sent the response_data")

        # Extract relevant information for JSON response
        # response_data["post_request_status_code"] = response.status
        response_data["post_request_content"] = post_req_text

        print("response sent successfully")

        # return jsonify(response_data)
        return jsonify(responseObj), 200

    except ValueError as e:
        # Log custom exceptions
        log_error(str(e))
        logger.error(f"ValueError: {str(e)}")
        return jsonify({"error": str(e)}), 400

    except CustomException as e:
        # Log custom exceptions
        log_error(str(e))
        logger.error(f"CustomException: {str(e)}")
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        # Log any other exceptions to the error.log file
        log_error(str(e))
        logger.error(f"An error occurred: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500
    

@app.route('/test', methods=['POST', "GET"])
def test():
    print("test successful")
    return jsonify({'status': 'success'})


@app.route('/process_video', methods=['POST'])
def process_video():
    try:
        # Get the S3 link from the request
        data = request.get_json()
        s3_video_url = data.get('s3_video_url')
        question_id = data.get('questionId')

        # Define paths
        local_video_path = "/Users/paragdarade/Desktop/mockAI/video_chunks/local_video.mp4"
        chunk_output_folder = "video_chunks"
        chunk_duration_seconds = 300

        # Download video from S3
        download_video_from_s3(s3_video_url, local_video_path)

        # Split the video into chunks
        split_video(local_video_path, chunk_output_folder, chunk_duration_seconds)

        # Generate transcript for each chunk
        transcripts = generate_video_transcript_from_chunks(chunk_output_folder)

        # Process or combine the individual transcripts as needed
        combined_transcript = "\n".join([f"Chunk {i + 1}:\n{transcript}" for i, transcript in enumerate(transcripts)])

        logger.info("Video processing completed.")

        print("Combined transcript: ", combined_transcript)

        analysis = analyze_interview_with_transcript(combined_transcript)
        
        print(analysis)


        # Perform POST request to the specified URL with the generated data
        backend_url = f"{BACKEND_URL}/feedback/{question_id}"
        feedback = analysis
          

        async def post_analysis():
            async with aiohttp.ClientSession() as session:
                async with session.post(backend_url, json=feedback) as post_req:
                    return await post_req.text()

        post_req_text = asyncio.run(post_analysis())

        print("Backend response:", post_req_text)

        return feedback


    except Exception as e:
        # Log any exceptions
        log_error(str(e))
        logger.error(f"An error occurred during video processing: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Internal Server Error'}), 500

if __name__ == '__main__':
    # Run the Flask app on all available network interfaces and port 5001
    app.run(host='0.0.0.0', port=5001)
