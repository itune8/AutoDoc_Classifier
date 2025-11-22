"""
Tests for utility functions.
"""
import pytest
from pathlib import Path
from app.utils import (
    sanitize_filename,
    truncate_text,
    format_timestamp,
    validate_file
)
from app.exceptions import UnsupportedFileTypeError

def test_sanitize_filename():
    """Test filename sanitization."""
    assert sanitize_filename("test file.pdf") == "test_file.pdf"
    assert sanitize_filename("../../../etc/passwd") == "passwd"
    assert sanitize_filename("file@#$.pdf") == "file___.pdf"

def test_truncate_text():
    """Test text truncation."""
    long_text = "a" * 200
    truncated = truncate_text(long_text, 50)
    assert len(truncated) == 50
    assert truncated.endswith("...")

def test_truncate_text_no_change():
    """Test that short text is not truncated."""
    short_text = "short"
    result = truncate_text(short_text, 50)
    assert result == short_text

def test_format_timestamp():
    """Test timestamp formatting."""
    from datetime import datetime
    dt = datetime(2024, 1, 15, 10, 30, 0)
    formatted = format_timestamp(dt)
    assert "2024-01-15" in formatted
    assert "10:30:00" in formatted
