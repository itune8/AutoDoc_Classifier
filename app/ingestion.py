import pdfplumber
from pathlib import Path

from PIL import Image
import pytesseract
from pytesseract import TesseractNotFoundError


def extract_text_from_file(path: str) -> str:
    file_path = Path(path)
    suffix = file_path.suffix.lower()
    if suffix == ".pdf":
        return _extract_text_from_pdf(file_path)
    if suffix in {".png", ".jpg", ".jpeg", ".bmp", ".tiff"}:
        return _extract_text_from_image(file_path)
    raise ValueError(f"Unsupported file type: {file_path.suffix}")


def _extract_text_from_pdf(path: Path) -> str:
    # First try standard text extraction
    text_parts: list[str] = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text_parts.append(page_text)

        combined = "\n".join(text_parts).strip()
        if combined:
            return combined

        # Fallback: OCR each page image when PDF has no embedded text
        ocr_parts: list[str] = []
        for page in pdf.pages:
            pil_image = page.to_image(resolution=300).original
            try:
                ocr_text = pytesseract.image_to_string(pil_image)
            except TesseractNotFoundError:
                ocr_text = ""
            ocr_parts.append(ocr_text or "")

    return "\n".join(ocr_parts)


def _extract_text_from_image(path: Path) -> str:
    image = Image.open(path)
    try:
        return pytesseract.image_to_string(image)
    except TesseractNotFoundError:
        # Gracefully handle missing Tesseract binary
        return ""
