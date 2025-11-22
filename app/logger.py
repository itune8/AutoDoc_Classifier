"""
Logging configuration and utilities for AutoDoc Classifier.
"""
import logging
import os
from pathlib import Path
from app.config import LOG_LEVEL, LOG_FILE, LOG_FORMAT

def setup_logging():
    """Initialize logging configuration."""
    # Create logs directory if it doesn't exist
    log_dir = Path(LOG_FILE).parent
    log_dir.mkdir(exist_ok=True)
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )

def get_logger(name):
    """Get a logger instance for a module."""
    return logging.getLogger(name)
