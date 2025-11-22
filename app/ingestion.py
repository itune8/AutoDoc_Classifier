import pdfplumber
from pathlib import Path
from PIL import Image
import pytesseract
from pytesseract import TesseractNotFoundError

from app.logger import get_logger
from app.exceptions import DocumentProcessingError, UnsupportedFileTypeError
from app.config import EXTRACT_TIMEOUT

logger = get_logger(__name__)


def extract_text_from_file(path: str) -> str:
    """
    Extract text from a document file.
    Supports PDF and image formats.
    """
    logger.info(f"Starting text extraction from: {path}")
    
    try:
        file_path = Path(path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        
        suffix = file_path.suffix.lower()
        
        if suffix == ".pdf":
            text = _extract_text_from_pdf(file_path)
        elif suffix in {".png", ".jpg", ".jpeg", ".bmp", ".tiff"}:
            text = _extract_text_from_image(file_path)
        else:
            raise UnsupportedFileTypeError(f"Unsupported file type: {file_path.suffix}")
        
        logger.info(f"Successfully extracted {len(text)} characters from {path}")
        return text
        
    except Exception as e:
        logger.error(f"Error extracting text from {path}: {str(e)}")
        raise DocumentProcessingError(f"Failed to extract text: {str(e)}")


def _extract_text_from_pdf(path: Path) -> str:
    """Extract text from PDF file with OCR fallback."""
    logger.debug(f"Extracting text from PDF: {path}")
    
    # First try standard text extraction
    text_parts: list[str] = []
    with pdfplumber.open(path) as pdf:
        logger.debug(f"PDF has {len(pdf.pages)} pages")
        
        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text() or ""
            text_parts.append(page_text)
            logger.debug(f"Page {i+1}: extracted {len(page_text)} characters")

        combined = "\n".join(text_parts).strip()
        if combined:
            logger.info("Successfully extracted text from PDF (native)")
            return combined

        # Fallback: OCR each page image when PDF has no embedded text
        logger.info("No embedded text found, attempting OCR")
        ocr_parts: list[str] = []
        for i, page in enumerate(pdf.pages):
            pil_image = page.to_image(resolution=300).original
            try:
                ocr_text = pytesseract.image_to_string(pil_image)
                logger.debug(f"OCR page {i+1}: extracted {len(ocr_text)} characters")
            except TesseractNotFoundError:
                logger.warning("Tesseract not found, OCR unavailable")
                ocr_text = ""
            ocr_parts.append(ocr_text or "")

    result = "\n".join(ocr_parts)
    logger.info(f"OCR extraction complete: {len(result)} characters")
    return result


def _extract_text_from_image(path: Path) -> str:
    """Extract text from image file using OCR."""
    logger.debug(f"Extracting text from image: {path}")
    
    try:
        image = Image.open(path)
        text = pytesseract.image_to_string(image)
        logger.info(f"OCR extraction from image: {len(text)} characters")
        return text
    except TesseractNotFoundError:
        logger.error("Tesseract not found, OCR unavailable")
        return ""
    except Exception as e:
        logger.error(f"Error during OCR: {str(e)}")
        raise DocumentProcessingError(f"OCR failed: {str(e)}")
