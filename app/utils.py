"""
Utility functions for AutoDoc Classifier.
"""
import hashlib
import mimetypes
from pathlib import Path
from datetime import datetime
from app.config import ALLOWED_EXTENSIONS, MAX_UPLOAD_SIZE
from app.exceptions import UnsupportedFileTypeError, FileSizeLimitError

def calculate_file_hash(file_path):
    """Calculate SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def validate_file(file_path):
    """Validate file type and size."""
    path = Path(file_path)
    
    # Check if file exists
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Check file extension
    if path.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise UnsupportedFileTypeError(
            f"File type {path.suffix} not supported. Allowed: {ALLOWED_EXTENSIONS}"
        )
    
    # Check file size
    file_size = path.stat().st_size
    if file_size > MAX_UPLOAD_SIZE:
        raise FileSizeLimitError(
            f"File size {file_size} bytes exceeds limit of {MAX_UPLOAD_SIZE} bytes"
        )
    
    return True

def get_mime_type(file_path):
    """Get MIME type of a file."""
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type or 'application/octet-stream'

def sanitize_filename(filename):
    """Sanitize filename for safe storage."""
    # Remove path components
    filename = Path(filename).name
    # Replace spaces and special characters
    safe_chars = '-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(c if c in safe_chars else '_' for c in filename)

def format_timestamp(dt=None):
    """Format datetime as ISO string."""
    if dt is None:
        dt = datetime.now()
    return dt.isoformat()

def truncate_text(text, max_length=100):
    """Truncate text to specified length."""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + '...'
