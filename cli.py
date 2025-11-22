#!/usr/bin/env python
"""
Command-line interface for AutoDoc Classifier.
"""
import argparse
import sys
from pathlib import Path

from app.logger import setup_logging, get_logger
from app.ingestion import extract_text_from_file
from app.classifier import classify_document, get_classification_confidence
from app.db import init_db, insert_document
from app.utils import validate_file
from app.config import DATABASE_PATH

setup_logging()
logger = get_logger(__name__)


def process_document(file_path: str, verbose: bool = False):
    """Process a single document."""
    try:
        if verbose:
            print(f"Processing: {file_path}")
        
        # Validate file
        validate_file(file_path)
        
        # Extract text
        text = extract_text_from_file(file_path)
        if verbose:
            print(f"Extracted {len(text)} characters")
        
        # Classify
        doc_type = classify_document(text)
        confidence = get_classification_confidence(text, doc_type)
        
        if verbose:
            print(f"Document Type: {doc_type}")
            print(f"Confidence: {confidence:.2%}")
        
        # Save to database
        doc_id = insert_document(file_path, doc_type, text)
        
        print(f"✓ Document processed successfully (ID: {doc_id})")
        return doc_id
        
    except Exception as e:
        logger.error(f"Error processing document: {str(e)}")
        print(f"✗ Error: {str(e)}", file=sys.stderr)
        return None


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AutoDoc Classifier - Automatic Document Classification"
    )
    
    parser.add_argument(
        'files',
        nargs='+',
        help='Document files to process'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )
    
    parser.add_argument(
        '--init-db',
        action='store_true',
        help='Initialize database before processing'
    )
    
    parser.add_argument(
        '--db-path',
        help='Database path (default: documents.db)'
    )
    
    args = parser.parse_args()
    
    # Initialize database
    if args.init_db:
        init_db()
        if args.verbose:
            print(f"Database initialized at: {DATABASE_PATH}")
    
    # Process each file
    success_count = 0
    for file_path in args.files:
        if not Path(file_path).exists():
            print(f"✗ File not found: {file_path}", file=sys.stderr)
            continue
        
        if process_document(file_path, args.verbose):
            success_count += 1
    
    # Summary
    total = len(args.files)
    print(f"\nProcessed {success_count}/{total} documents successfully")
    
    return 0 if success_count == total else 1


if __name__ == '__main__':
    sys.exit(main())
