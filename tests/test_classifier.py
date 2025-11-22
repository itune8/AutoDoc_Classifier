"""
Tests for document classifier.
"""
import pytest
from app.classifier import classify_document, get_classification_confidence

def test_classify_invoice():
    """Test invoice classification."""
    text = "INVOICE #12345\nInvoice Date: 2024-01-15\nTotal Amount: $1000.00"
    result = classify_document(text)
    assert result == "invoice"

def test_classify_purchase_order():
    """Test purchase order classification."""
    text = "Purchase Order PO-98765\nQuantity: 100\nTotal: $5000"
    result = classify_document(text)
    assert result == "purchase_order"

def test_classify_paystub():
    """Test paystub classification."""
    text = "Pay Stub for Employee\nGross Pay: $3000\nDeductions: $500"
    result = classify_document(text)
    assert result == "pay_stub"

def test_classify_unknown():
    """Test unknown document classification."""
    text = "This is just random text without any keywords"
    result = classify_document(text)
    assert result == "unknown"

def test_confidence_scoring():
    """Test confidence scoring for classification."""
    text = "INVOICE #12345\nInvoice Number: INV-001\nBill To: Customer\nTotal Amount: $1000"
    confidence = get_classification_confidence(text, "invoice")
    assert confidence > 0.5
    assert confidence <= 1.0

def test_confidence_low_for_wrong_type():
    """Test that confidence is low for incorrect classification."""
    text = "INVOICE #12345"
    confidence = get_classification_confidence(text, "purchase_order")
    assert confidence < 0.5
