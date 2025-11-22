import sys
from pathlib import Path

from app.ingestion import extract_text_from_file
from app.classifier import classify_document
from app.extractors.invoice_extractor import extract_invoice_fields
from app.extractors.po_extractor import extract_po_fields
from app.db import init_db, insert_document, insert_invoice, insert_purchase_order


def process_file(file_path: str) -> None:
    text = extract_text_from_file(file_path)
    doc_type = classify_document(text)

    document_id = insert_document(file_path=file_path, document_type=doc_type, text=text)

    if doc_type == "invoice":
        fields = extract_invoice_fields(text)
        insert_invoice(document_id, fields)
        print(f"Processed invoice: {fields}")

    elif doc_type == "purchase_order":
        fields = extract_po_fields(text)
        insert_purchase_order(document_id, fields)
        print(f"Processed purchase order: {fields}")

    else:
        print(f"Unsupported or unknown document type for file: {file_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m app.main <path-to-document.pdf>")
        sys.exit(1)

    init_db()
    path = Path(sys.argv[1]).resolve()
    if not path.exists():
        print(f"File does not exist: {path}")
        sys.exit(1)

    process_file(str(path))
