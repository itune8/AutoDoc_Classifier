"""
Custom exceptions for AutoDoc Classifier.
"""

class AutoDocException(Exception):
    """Base exception for AutoDoc Classifier."""
    pass

class DocumentProcessingError(AutoDocException):
    """Raised when document processing fails."""
    pass

class ExtractionError(AutoDocException):
    """Raised when field extraction fails."""
    pass

class ClassificationError(AutoDocException):
    """Raised when document classification fails."""
    pass

class DatabaseError(AutoDocException):
    """Raised when database operations fail."""
    pass

class ValidationError(AutoDocException):
    """Raised when document validation fails."""
    pass

class UnsupportedFileTypeError(AutoDocException):
    """Raised when file type is not supported."""
    pass

class FileSizeLimitError(AutoDocException):
    """Raised when file size exceeds the limit."""
    pass
