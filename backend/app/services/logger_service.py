import os
import logging
from logging.handlers import RotatingFileHandler

class LoggerService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._init_logger(*args, **kwargs)
        return cls._instance

    def _init_logger(
        self, 
        log_dir: str = "./logs", 
        log_file: str = "queries.log", 
        max_bytes: int = 5 * 1024 * 1024,  # 5 MB
        backup_count: int = 3
    ):
        os.makedirs(log_dir, exist_ok=True)
        self.log_path = os.path.join(log_dir, log_file)

        self.logging = logging.getLogger("RAGLogger")
        self.logging.setLevel(logging.INFO)
        self.logging.propagate = False  # prevent double logging

        # Rotating file handler
        file_handler = RotatingFileHandler(
            self.log_path, maxBytes=max_bytes, backupCount=backup_count
        )
        file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_formatter)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(file_formatter)

        # Add handlers if not already added
        if not self.logging.handlers:
            self.logging.addHandler(file_handler)
            self.logging.addHandler(console_handler)

    def log(self, message: str):
        """Generic log method for any message."""
        self.logging.info(message)

