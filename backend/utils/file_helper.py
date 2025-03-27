import os
import logging
import chardet
from .logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

def read_file_to_string(file_path):
    try:
        # Use raw string or forward slashes for compatibility
        file_path = os.path.join(os.getcwd(), file_path)
        
        with open(file_path, 'rb') as file:
            raw_data = file.read()
            encoding = chardet.detect(raw_data)['encoding']
            logger.info(f"encoding = {encoding}")
        
        with open(file_path, 'r', encoding=encoding) as file:
            file_content = file.read()
        return file_content
    except FileNotFoundError:
        logger.info(f"Error: The file at {file_path} was not found.")
        return None
    except Exception as e:
        logger.info(f"An error occurred: {e}")
        return None