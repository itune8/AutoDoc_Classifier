"""
Document validators for AutoDoc Classifier.
"""
from app.logger import get_logger
from app.exceptions import ValidationError

logger = get_logger(__name__)

class DocumentValidator:
    """Base validator for documents."""
    
    def __init__(self, document_text):
        self.text = document_text
        self.errors = []
    
    def validate(self):
        """Perform validation checks."""
        raise NotImplementedError("Subclasses must implement validate()")
    
    def is_valid(self):
        """Check if document is valid."""
        self.validate()
        return len(self.errors) == 0
    
    def add_error(self, error_msg):
        """Add validation error."""
        self.errors.append(error_msg)
        logger.warning(f"Validation error: {error_msg}")

class InvoiceValidator(DocumentValidator):
    """Validator for invoice documents."""
    
    def validate(self):
        """Validate invoice structure."""
        if not self.text or len(self.text.strip()) < 50:
            self.add_error("Invoice text too short")
        
        # Check for required keywords
        required_keywords = ['invoice', 'total', 'amount']
        for keyword in required_keywords:
            if keyword.lower() not in self.text.lower():
                self.add_error(f"Missing required keyword: {keyword}")
        
        return self.is_valid()

class PurchaseOrderValidator(DocumentValidator):
    """Validator for purchase order documents."""
    
    def validate(self):
        """Validate purchase order structure."""
        if not self.text or len(self.text.strip()) < 50:
            self.add_error("Purchase order text too short")
        
        # Check for required keywords
        required_keywords = ['purchase order', 'po', 'quantity']
        keyword_found = any(kw.lower() in self.text.lower() for kw in required_keywords)
        
        if not keyword_found:
            self.add_error("Missing purchase order keywords")
        
        return self.is_valid()

class PaystubValidator(DocumentValidator):
    """Validator for paystub documents."""
    
    def validate(self):
        """Validate paystub structure."""
        if not self.text or len(self.text.strip()) < 50:
            self.add_error("Paystub text too short")
        
        # Check for required keywords
        required_keywords = ['pay', 'earnings', 'deductions', 'gross']
        keyword_count = sum(1 for kw in required_keywords if kw.lower() in self.text.lower())
        
        if keyword_count < 2:
            self.add_error("Insufficient paystub keywords found")
        
        return self.is_valid()

def get_validator(document_type):
    """Get appropriate validator for document type."""
    validators = {
        'invoice': InvoiceValidator,
        'purchase_order': PurchaseOrderValidator,
        'paystub': PaystubValidator,
    }
    
    return validators.get(document_type, DocumentValidator)
