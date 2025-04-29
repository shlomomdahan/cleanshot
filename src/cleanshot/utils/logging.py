import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def configure_logging():
    """
    Configure logging for the entire application.
    This should be called once at application startup.
    """
    # Create the logs directory
    log_dir = Path.home() / ".cleanshot"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "cleanshot.log"

    # Create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Setup file handler
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=1024 * 1024,  # 1MB
        backupCount=5,
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Configure root logger for the 'cleanshot' package
    root_logger = logging.getLogger("cleanshot")
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)

    # Return the log file path for reference
    return log_file
