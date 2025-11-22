import re
from typing import Any, Dict


def extract_invoice_fields(text: str) -> Dict[str, Any]:
    fields: Dict[str, Any] = {}

    invoice_number_match = re.search(
        r"(invoice\s*number|inv\s*no\.?)\s*[:\-]?\s*([A-Za-z0-9\-]+)",
        text,
        re.IGNORECASE,
    )
    if invoice_number_match:
        fields["invoice_number"] = invoice_number_match.group(2).strip()

    date_match = re.search(
        r"(invoice\s*date|date)\s*[:\-]?\s*([0-9]{2,4}[\/\-][0-9]{1,2}[\/\-][0-9]{1,2})",
        text,
        re.IGNORECASE,
    )
    if date_match:
        fields["invoice_date"] = date_match.group(2).strip()

    total_match = re.search(
        r"(total\s*amount|amount\s*due|total)\s*[:\-]?\s*([$€£]?\s*[0-9\.,]+)",
        text,
        re.IGNORECASE,
    )
    if total_match:
        fields["total_amount"] = total_match.group(2).strip()

    vendor_match = re.search(
        r"(from|vendor|supplier)\s*[:\-]?\s*([A-Za-z0-9 &.,]+)",
        text,
        re.IGNORECASE,
    )
    if vendor_match:
        fields["vendor_name"] = vendor_match.group(2).strip()

    return fields
