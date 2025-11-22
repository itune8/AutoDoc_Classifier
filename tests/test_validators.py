"""
Tests for document validators.
"""
import pytest
from app.validators import (
    InvoiceValidator,
    PurchaseOrderValidator,
    PaystubValidator,
    get_validator
)

def test_invoice_validator_valid():
    """Test valid invoice validation."""
    text = "INVOICE #12345\nTotal Amount: $1000\nInvoice Date: 2024-01-15"
    validator = InvoiceValidator(text)
    assert validator.is_valid() is True
    assert len(validator.errors) == 0

def test_invoice_validator_invalid():
    """Test invalid invoice validation."""
    text = "Short text"
    validator = InvoiceValidator(text)
    assert validator.is_valid() is False
    assert len(validator.errors) > 0

def test_po_validator_valid():
    """Test valid purchase order validation."""
    text = "Purchase Order PO-12345\nQuantity: 100\nUnit Price: $50"
    validator = PurchaseOrderValidator(text)
    assert validator.is_valid() is True

def test_paystub_validator_valid():
    """Test valid paystub validation."""
    text = "Employee Pay Stub\nGross Pay: $3000\nEarnings YTD: $36000\nDeductions: $500"
    validator = PaystubValidator(text)
    assert validator.is_valid() is True

def test_get_validator():
    """Test validator factory function."""
    invoice_validator = get_validator('invoice')
    assert invoice_validator == InvoiceValidator
    
    po_validator = get_validator('purchase_order')
    assert po_validator == PurchaseOrderValidator
