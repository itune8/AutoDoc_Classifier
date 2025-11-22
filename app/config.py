"""
Configuration settings for AutoDoc Classifier.
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database settings
DATABASE_PATH = os.getenv('DATABASE_PATH', BASE_DIR / 'documents.db')
DATABASE_BACKUP_DIR = BASE_DIR / 'backups'

# Upload settings
UPLOAD_FOLDER = BASE_DIR / 'uploads'
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'.pdf', '.jpg', '.jpeg', '.png'}

# Document processing settings
EXTRACT_TIMEOUT = 30  # seconds
MAX_TEXT_LENGTH = 1000000  # characters

# Classification settings
CONFIDENCE_THRESHOLD = 0.7
DEFAULT_DOCUMENT_TYPE = 'unknown'

# Logging settings
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = BASE_DIR / 'logs' / 'autodoc.log'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Web server settings
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Feature flags
ENABLE_OCR = os.getenv('ENABLE_OCR', 'False').lower() == 'true'
ENABLE_BATCH_PROCESSING = True
ENABLE_ASYNC_PROCESSING = False
