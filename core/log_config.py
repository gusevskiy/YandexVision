import os
from loguru import logger

def setup_logger():
    log_directory = os.path.join(os.getcwd(), "logs")
    os.makedirs(log_directory, exist_ok=True)  # Создаёт директорию, если она ещё не существует
    logger.add(
        os.path.join(log_directory, "file_{time:YYYY-MM-DD}.log"), 
        rotation="1 day", 
        level="DEBUG"
    )