import re
from typing import Any, Dict


def extract_po_fields(text: str) -> Dict[str, Any]:
    fields: Dict[str, Any] = {}

    po_number_match = re.search(
        r"(po\s*number|purchase\s*order\s*no\.?)\s*[:\-]?\s*([A-Za-z0-9\-]+)",
        text,
        re.IGNORECASE,
    )
    if po_number_match:
        fields["po_number"] = po_number_match.group(2).strip()

    date_match = re.search(
        r"(po\s*date|date)\s*[:\-]?\s*([0-9]{2,4}[\/\-][0-9]{1,2}[\/\-][0-9]{1,2})",
        text,
        re.IGNORECASE,
    )
    if date_match:
        fields["po_date"] = date_match.group(2).strip()

    total_match = re.search(
        r"(total\s*amount|amount)\s*[:\-]?\s*([$€£]?\s*[0-9\.,]+)",
        text,
        re.IGNORECASE,
    )
    if total_match:
        fields["total_amount"] = total_match.group(2).strip()

    buyer_match = re.search(
        r"(to|buyer|customer)\s*[:\-]?\s*([A-Za-z0-9 &.,]+)",
        text,
        re.IGNORECASE,
    )
    if buyer_match:
        fields["buyer_name"] = buyer_match.group(2).strip()

    return fields
