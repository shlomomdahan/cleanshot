import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def configure_logging():
    log_file = Path.home() / ".cleanshot.log"

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=1024 * 1024,  # 1MB
        backupCount=5,
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    root_logger = logging.getLogger("cleanshot")

    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)

    return log_file


def clear_logs():
    log_file = Path.home() / ".cleanshot.log"
    if log_file.exists():
        open(log_file, "w").close()
