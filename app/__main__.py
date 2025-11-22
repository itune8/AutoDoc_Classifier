"""
Entry point for running the AutoDoc Classifier as a module.
Usage: python -m app <path-to-document>
"""
import sys
from pathlib import Path
from app.ingestion import extract_text_from_file
from app.classifier import classify_document
from app.extractors.invoice_extractor import extract_invoice_fields
from app.extractors.po_extractor import extract_po_fields
from app.extractors.paystub_extractor import extract_paystub_fields
from app.extractors.id_extractor import extract_id_fields
from app.extractors.flood_form_extractor import extract_flood_form_fields
from app.db import init_db, insert_document


def main():
    """Main entry point for document processing."""
    if len(sys.argv) < 2:
        print("AutoDoc Classifier - Automatic Document Classification and Field Extraction")
        print("\nUsage: python -m app <path-to-document>")
        print("\nSupported document types:")
        print("  - Invoices")
        print("  - Purchase Orders")
        print("  - Paystubs")
        print("  - ID Documents")
        print("  - Flood Forms")
        sys.exit(1)

    init_db()
    file_path = Path(sys.argv[1]).resolve()
    
    if not file_path.exists():
        print(f"Error: File does not exist: {file_path}")
        sys.exit(1)

    # Import and use the process_file function from main
    from app.main import process_file
    process_file(str(file_path))


if __name__ == "__main__":
    main()
