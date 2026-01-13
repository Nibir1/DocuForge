import logging
import sys
from app.core.config import settings

def setup_logging():
    """
    Configures the root logger for the application.
    Sets log level based on environment settings.
    """
    
    # Determine Log Level
    log_level = logging.DEBUG if settings.ENVIRONMENT == "dev" else logging.INFO
    
    # Create Formatter
    # Format: [Time] [Level] [Module:Line] - Message
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(module)s:%(lineno)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Configure Stream Handler (Console)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Get Root Logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Avoid adding duplicate handlers if re-initialized
    if not root_logger.handlers:
        root_logger.addHandler(console_handler)
    
    # Set levels for noisy libraries to WARNING to keep logs clean
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("qdrant_client").setLevel(logging.WARNING)

    return root_logger

# Initialize immediately when module is imported
logger = setup_logging()