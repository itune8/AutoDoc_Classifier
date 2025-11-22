from typing import Literal

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
    lower = text.lower()

    if "pay stub" in lower or "gross pay" in lower:
        return "pay_stub"

    if "standard flood hazard determination form" in lower or "federal emergency management agency" in lower:
        return "flood_form"

    if "w-2" in lower or "form w-2" in lower or "w2 wage and tax statement" in lower:
        return "w2"

    if "passport" in lower and "united states of america" in lower:
        return "passport"

    if "driver license" in lower or "driver's license" in lower or "driver licence" in lower or "dl number" in lower:
        return "driver_license"

    if "invoice" in lower or "invoice number" in lower:
        return "invoice"

    if "purchase order" in lower or "po number" in lower:
        return "purchase_order"

    return "unknown"
