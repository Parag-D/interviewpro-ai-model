# s3_operation.py

import io
import boto3
import sys
import os
from exception import CustomException
from logger import create_logs, log_error
from dotenv import find_dotenv, load_dotenv

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

# async def upload_to_s3(question, response_content):
#     try:
#         s3_key = f"audio/{question.replace(' ', '_')}.mp3"
#         # await boto3.client.upload_fileobj(io.BytesIO(response_content), S3_BUCKET_NAME, s3_key)
#         # return f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_key}"

#         s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION)

#         # Upload the file to S3
#         s3_client.upload_fileobj(io.BytesIO(response_content), S3_BUCKET_NAME, s3_key)

#         # Get the S3 URL for the uploaded file
#         s3_url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_key}"

#         return s3_url


#     # except Exception as e:
#     #     raise CustomException("Error uploading to S3", error_detail=sys.exc_info())
    
#     except Exception as e:
#         # Log the error and raise a CustomException
#         raise CustomException("Error uploading to S3", error_detail=str(e))

    
import re
import urllib.parse

def upload_to_s3(question, response_content):
    try:
        print("inside upload to s3 baby...")
        # Remove special characters from the question
        cleaned_question = re.sub(r'[^a-zA-Z0-9 ]', '', question)

        # Replace spaces with underscores
        cleaned_question = cleaned_question.replace(' ', '_')

        # URL encode the cleaned question to handle special characters
        encoded_question = urllib.parse.quote(cleaned_question, safe='')

        # Construct the S3 key
        s3_key = f"audio/{encoded_question}.mp3"

        s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION)

        # Upload the file to S3
        s3_client.upload_fileobj(io.BytesIO(response_content), S3_BUCKET_NAME, s3_key)

        # Get the S3 URL for the uploaded file
        s3_url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_key}"
        print("Getting out of upload to s3 baby")
        return s3_url

    except Exception as e:
        log_error(f"S3 upload failed for question: {question}. Error: {str(e)}")
        raise CustomException("Error uploading to S3", error_detail=str(e))
    except Exception as e:
        log_error(f"Unexpected error uploading to S3 for question: {question}. Error: {str(e)}")
        raise CustomException("Unexpected error uploading to S3", error_detail=str(e))
