import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


class Logger:
    _instance: Optional[logging.Logger] = None

    @classmethod
    def get_logger(cls, name: str = "cleanshot") -> logging.Logger:
        if cls._instance is None:
            cls._instance = cls._setup_logging(name)
        return cls._instance

    @staticmethod
    def _setup_logging(name: str) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        log_dir = Path.home() / ".cleanshot"
        log_dir.mkdir(parents=True, exist_ok=True)

        # File handler with rotation
        file_handler = RotatingFileHandler(
            log_dir / "cleanshot.log",
            maxBytes=1024 * 1024,  # 1MB
            backupCount=5,
        )
        file_handler.setLevel(logging.DEBUG)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)

        # Create formatters and add them to the handlers
        file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        console_formatter = logging.Formatter("%(levelname)s: %(message)s")

        file_handler.setFormatter(file_formatter)
        console_handler.setFormatter(console_formatter)

        # Add the handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger
