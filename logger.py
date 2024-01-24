# logger.py 

import os
import sys
import logging
from datetime import datetime, timedelta
from exception import CustomException
from dotenv import load_dotenv
from logging import Handler
import boto3
from botocore.exceptions import ClientError

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_CLOUDWATCH_GROUP_NAME = os.getenv("AWS_CLOUDWATCH_GROUP_NAME")

class CloudWatchLogsHandler(Handler):
    def __init__(self, log_group_name, log_stream_name):
        super().__init__()
        self.log_group_name = log_group_name
        self.log_stream_name = log_stream_name
        self.client = boto3.client('logs', region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

        # Try to create log stream, catch exception if it already exists
        try:
            self.client.create_log_stream(
                logGroupName=self.log_group_name,
                logStreamName=self.log_stream_name
            )
        except ClientError as e:
            if e.response['Error']['Code'] != 'ResourceAlreadyExistsException':
                # Log an error if it's not a ResourceAlreadyExistsException
                self.handleError(e)

    def emit(self, record):
        try:
            log_event = {
                'timestamp': int(record.created * 1000),
                'message': self.format(record)
            }

            self.client.put_log_events(
                logGroupName=self.log_group_name,
                logStreamName=self.log_stream_name,
                logEvents=[log_event]
            )
        except Exception as e:
            self.handleError(record)


def create_logs():
    logger = logging.getLogger(__name__)

    # For Local system
    LOG_FILE_FOLDER = f"{datetime.now().strftime('%m_%d_%Y')}"
    LOG_FILE = f"{datetime.now().strftime('%H:%M:%S')}.log"
    logs_path = os.path.join(os.getcwd(), 'logs', LOG_FILE_FOLDER)
    os.makedirs(logs_path, exist_ok=True)

    LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

    logging.basicConfig(
        filename=LOG_FILE_PATH,
        format="[%(asctime)s] %(lineno)d - %(filename)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s",
        level=logging.INFO,
    )

    cloudwatch_handler = CloudWatchLogsHandler(AWS_CLOUDWATCH_GROUP_NAME, LOG_FILE_FOLDER)
    
    try:
        # Add handler
        logger.addHandler(cloudwatch_handler)

        # Set the logger level
        logger.setLevel(logging.INFO)
        
        # Cleanup old logs
        cleanup_old_logs()

        return logger

    except Exception as e:
        logger.error(f"An error occurred: {CustomException(e,sys)}")


def cleanup_old_logs():
    """
    Deletes old log files and folders that are more than 4 days old.

    This function iterates over the directories in the 'logs' folder and checks if each folder represents a valid date. If a folder is older than 7 days, it deletes all the files inside the folder and then deletes the folder itself.

    Parameters:
    None

    Returns:
    None
    """
    logs_directory = os.path.join(os.getcwd(), 'logs')
    for folder_name in os.listdir(logs_directory):
        folder_path = os.path.join(logs_directory, folder_name)
        if os.path.isdir(folder_path):
            try:
                folder_date = datetime.strptime(folder_name, '%m_%d_%Y')
                if datetime.now() - folder_date > timedelta(days=4):
                    # Folder is older than 7 days, delete it and its contents
                    for file_name in os.listdir(folder_path):
                        file_path = os.path.join(folder_path, file_name)
                        try:
                            os.remove(file_path)
                        except Exception as e:
                            logging.info(
                                f"Error deleting file {file_path}: {e}")
                    try:
                        os.rmdir(folder_path)
                    except Exception as e:
                        logging.info(
                            f"Error deleting folder {folder_path}: {e}")
            except ValueError:
                # Ignore folders with invalid date format
                pass



def log_error(error_message):
    logger = logging.getLogger(__name__)
    
    if isinstance(error_message, tuple):
        # If error_message is a tuple, extract the string representation
        error_message = str(error_message)

    logger.error(f"{error_message}", exc_info=True)

