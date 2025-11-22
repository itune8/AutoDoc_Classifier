import re
from typing import Dict, Any


def extract_flood_form_fields(text: str) -> Dict[str, Any]:
    fields: Dict[str, Any] = {}

    # Borrower name (e.g., KIRSHENBAUM, AHARON)
    borrower_match = re.search(r"borrower\s*:?\s*([A-Z ,'-]+)", text, re.IGNORECASE)
    if borrower_match:
        fields["borrower"] = borrower_match.group(1).strip()

    # Lender / Federal Savings Bank style
    lender_match = re.search(r"the federal savings bank", text, re.IGNORECASE)
    if lender_match:
        fields["lender"] = "The Federal Savings Bank"

    # Property / collateral address: grab the line after "Address Determination Address:"
    addr_block_match = re.search(
        r"Address Determination Address:\s*(.+)", text, re.IGNORECASE
    )
    if addr_block_match:
        fields["determination_address"] = addr_block_match.group(1).strip()

    # County (e.g., OCEAN COUNTY)
    county_match = re.search(r"([A-Z ]+COUNTY)", text)
    if county_match:
        fields["county"] = county_match.group(1).strip()

    # FEMA / Form identifier
    if "standard flood hazard determination form" in text.lower():
        fields["form_type"] = "Standard Flood Hazard Determination Form"

    return fields
