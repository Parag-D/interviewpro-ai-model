# exception.py

import sys

def error_message_detail(error, error_detail):
    """
    Generate a detailed error message.

    Args:
        error: The error that occurred.
        error_detail: The detailed information about the error.

    Returns:
        The detailed error message including the file name, line number, and error message.
    """
    file_name = error_detail.tb_frame.f_code.co_filename
    error_message = "error occurred in python script name [{0}] line number [{1}] error message[{2}]".format(
        file_name, error_detail.tb_lineno, str(error)
    )
    return error_message

class CustomException(Exception):
    def __init__(self, error_message, error_detail):
        super().__init__(error_message)
        self.error_message = error_message_detail(
            error_message, error_detail=error_detail)

    def __str__(self) -> str:
        return self.error_message
