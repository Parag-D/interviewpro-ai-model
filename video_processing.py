# generate_video_transcript_from_chunks

import os
import requests
from moviepy.video.io.VideoFileClip import VideoFileClip
import asyncio
from openai import OpenAI  # Use synchronous OpenAI client
from dotenv import find_dotenv, load_dotenv
from logger import create_logs, log_error

# Load environment variables
load_dotenv(find_dotenv())

# Set up logging
logger = create_logs()

# Set up OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Use synchronous OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def split_video(input_video, output_folder, chunk_duration):
    try:
        os.makedirs(output_folder, exist_ok=True)

        video_clip = VideoFileClip(input_video)
        start_time = 0
        end_time = start_time + chunk_duration

        chunk_number = 1
        while end_time < video_clip.duration:
            # Create a subclip
            subclip = video_clip.subclip(start_time, end_time)

            # Export the subclip to a file
            chunk_filename = f"{output_folder}/chunk_{chunk_number}.mp4"
            subclip.write_videofile(chunk_filename, codec="libx264", audio_codec="aac")

            # Move to the next chunk
            start_time = end_time
            end_time += chunk_duration
            chunk_number += 1

        video_clip.close()
        logger.info("Video splitting completed.")

    except Exception as e:
        # Log any exceptions
        log_error(str(e))
        logger.error(f"An error occurred during video splitting: {str(e)}")

def download_video_from_s3(s3_url, local_path):
    try:
        logger.info("Downloading video from S3...")
        response = requests.get(s3_url, stream=True)
        
        if response.status_code == 200:
            with open(local_path, 'wb') as video_file:
                for chunk in response.iter_content(chunk_size=1024):
                    video_file.write(chunk)
            logger.info("Download complete")
        else:
            raise ValueError(f"Failed to download video. Status code: {response.status_code}")

    except Exception as e:
        # Log any exceptions
        log_error(str(e))
        logger.error(f"An error occurred during video download: {str(e)}")


def generate_video_transcript_from_chunks(chunks_folder):
    transcripts = []

    try:
        for chunk_file in sorted(os.listdir(chunks_folder)):
            if chunk_file.endswith(".mp4"):
                chunk_path = os.path.join(chunks_folder, chunk_file)
                logger.info(f"Transcribing {chunk_file}...")

                try:
                    # Transcribe audio using Whisper ASR model
                    with open(chunk_path, "rb") as file:
                        transcription = client.audio.transcriptions.create(
                            model="whisper-1", 
                            file=file
                        )

                    transcript_text = transcription.text
                    transcripts.append(transcript_text)
                    logger.info(f"Transcription for {chunk_file}:\n{transcript_text}")

                except Exception as e:
                    # Handle exceptions as needed
                    log_error(str(e))
                    logger.error(f"Error during transcription for {chunk_file}: {str(e)}")

    except Exception as e:
        # Log any exceptions
        log_error(str(e))
        logger.error(f"An error occurred during transcription: {str(e)}")

    return transcripts
