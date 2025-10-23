import logging
import sys
from functools import wraps
from app.utils.config import LOG_LEVEL, LOG_FILE, LOG_ROTATION, LOG_RETENTION

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


def get_logger(name: str):
    return logging.getLogger(name)


def log_operation(operation_name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = get_logger(func.__module__)
            logger.info(f"Starting operation: {operation_name}")
            try:
                result = func(*args, **kwargs)
                logger.info(f"Finished operation: {operation_name} successfully")
                return result
            except Exception as e:
                logger.exception(f"Error during operation: {operation_name} - {e}")
                raise

        return wrapper

    return decorator