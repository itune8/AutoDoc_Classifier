import re
from typing import Dict, Any


def extract_driver_license_fields(text: str) -> Dict[str, Any]:
    fields: Dict[str, Any] = {}

    # Name (very naive, based on SAMPLE JELANI style)
    name_match = re.search(r"sample\s+([A-Z][a-zA-Z]+)", text, re.IGNORECASE)
    if name_match:
        fields["name"] = name_match.group(1).strip()

    dl_match = re.search(r"DLN?\s*([A-Z0-9]+)", text, re.IGNORECASE)
    if dl_match:
        fields["dl_number"] = dl_match.group(1).strip()

    dob_match = re.search(r"DOB\s*([0-9]{2}\/[0-9]{2}\/[0-9]{4})", text, re.IGNORECASE)
    if dob_match:
        fields["DOB"] = dob_match.group(1).strip()

    return fields


def extract_passport_fields(text: str) -> Dict[str, Any]:
    fields: Dict[str, Any] = {}

    # Extremely simplified examples
    number_match = re.search(r"passport\s*no\.?\s*([A-Z0-9]+)", text, re.IGNORECASE)
    if number_match:
        fields["passport_number"] = number_match.group(1).strip()

    name_match = re.search(r"(?:surname|last name)\s*[:]?\s*([A-Z][A-Za-z ]+)", text, re.IGNORECASE)
    if name_match:
        fields["name"] = name_match.group(1).strip()

    return fields


def extract_w2_fields(text: str) -> Dict[str, Any]:
    fields: Dict[str, Any] = {}

    ssn_match = re.search(r"social security number\s*([0-9]{3}-[0-9]{2}-[0-9]{4})", text, re.IGNORECASE)
    if ssn_match:
        fields["ssn"] = ssn_match.group(1).strip()

    wages_match = re.search(r"1\s*wages, tips, other compensation\s*([0-9,.]+)", text, re.IGNORECASE)
    if wages_match:
        fields["wages"] = wages_match.group(1).strip()

    ein_match = re.search(r"employer identification number \(ein\)\s*([0-9\-]+)", text, re.IGNORECASE)
    if ein_match:
        fields["ein"] = ein_match.group(1).strip()

    return fields
