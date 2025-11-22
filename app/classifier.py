from typing import Literal, Dict
from app.logger import get_logger
from app.config import CONFIDENCE_THRESHOLD

logger = get_logger(__name__)

DocumentType = Literal[
    "invoice",
    "purchase_order",
    "driver_license",
    "passport",
    "w2",
    "pay_stub",
    "flood_form",
    "unknown",
]


def classify_document(text: str) -> DocumentType:
    """
    Classify document based on text content.
    Returns the most likely document type.
    """
    lower = text.lower()
    logger.info(f"Classifying document with text length: {len(text)}")

    if "pay stub" in lower or "gross pay" in lower:
        logger.info("Classified as pay_stub")
        return "pay_stub"

    if "standard flood hazard determination form" in lower or "federal emergency management agency" in lower:
        logger.info("Classified as flood_form")
        return "flood_form"

    if "w-2" in lower or "form w-2" in lower or "w2 wage and tax statement" in lower:
        logger.info("Classified as w2")
        return "w2"

    if "passport" in lower and "united states of america" in lower:
        logger.info("Classified as passport")
        return "passport"

    if "driver license" in lower or "driver's license" in lower or "driver licence" in lower or "dl number" in lower:
        logger.info("Classified as driver_license")
        return "driver_license"

    if "invoice" in lower or "invoice number" in lower:
        logger.info("Classified as invoice")
        return "invoice"

    if "purchase order" in lower or "po number" in lower:
        logger.info("Classified as purchase_order")
        return "purchase_order"

    logger.warning("Document type unknown")
    return "unknown"


def get_classification_confidence(text: str, doc_type: DocumentType) -> float:
    """
    Calculate confidence score for a classification.
    Returns a value between 0 and 1.
    """
    lower = text.lower()
    
    keyword_map = {
        "pay_stub": ["pay stub", "gross pay", "net pay", "deductions", "earnings"],
        "flood_form": ["flood hazard", "fema", "federal emergency"],
        "w2": ["w-2", "form w-2", "wage and tax"],
        "passport": ["passport", "united states of america", "date of birth"],
        "driver_license": ["driver license", "driver's license", "dl number"],
        "invoice": ["invoice", "invoice number", "bill to", "total amount"],
        "purchase_order": ["purchase order", "po number", "quantity", "unit price"],
    }
    
    if doc_type not in keyword_map:
        return 0.0
    
    keywords = keyword_map[doc_type]
    matches = sum(1 for keyword in keywords if keyword in lower)
    
    confidence = min(matches / len(keywords), 1.0)
    logger.debug(f"Classification confidence for {doc_type}: {confidence:.2f}")
    
    return confidence
