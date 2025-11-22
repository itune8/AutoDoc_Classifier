"""
REST API for AutoDoc Classifier using Flask.
"""
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from pathlib import Path

from app.config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, MAX_UPLOAD_SIZE
from app.ingestion import extract_text_from_file
from app.classifier import classify_document, get_classification_confidence
from app.db import init_db, insert_document
from app.utils import validate_file, get_mime_type, calculate_file_hash
from app.logger import setup_logging, get_logger
from app.exceptions import AutoDocException

setup_logging()
logger = get_logger(__name__)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_UPLOAD_SIZE
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
Path(UPLOAD_FOLDER).mkdir(exist_ok=True)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'AutoDoc Classifier API'
    })

@app.route('/api/v1/classify', methods=['POST'])
def classify():
    """
    Classify uploaded document and extract fields.
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = Path(UPLOAD_FOLDER) / filename
        file.save(filepath)
        
        logger.info(f"Processing uploaded file: {filename}")
        
        # Validate file
        validate_file(filepath)
        
        # Extract text
        text = extract_text_from_file(str(filepath))
        
        # Classify document
        doc_type = classify_document(text)
        confidence = get_classification_confidence(text, doc_type)
        
        # Calculate file hash
        file_hash = calculate_file_hash(filepath)
        
        # Store in database
        document_id = insert_document(
            file_path=str(filepath),
            document_type=doc_type,
            text=text
        )
        
        return jsonify({
            'success': True,
            'document_id': document_id,
            'document_type': doc_type,
            'confidence': confidence,
            'file_hash': file_hash,
            'text_length': len(text)
        }), 200
        
    except AutoDocException as e:
        logger.error(f"AutoDoc error: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/v1/documents', methods=['GET'])
def list_documents():
    """List all processed documents."""
    try:
        from app.db import get_all_documents
        documents = get_all_documents()
        return jsonify({
            'success': True,
            'count': len(documents),
            'documents': documents
        }), 200
    except Exception as e:
        logger.error(f"Error listing documents: {str(e)}")
        return jsonify({'error': 'Failed to retrieve documents'}), 500

@app.route('/api/v1/documents/<int:doc_id>', methods=['GET'])
def get_document(doc_id):
    """Get a specific document by ID."""
    try:
        from app.db import get_document_by_id
        document = get_document_by_id(doc_id)
        
        if not document:
            return jsonify({'error': 'Document not found'}), 404
        
        return jsonify({
            'success': True,
            'document': document
        }), 200
    except Exception as e:
        logger.error(f"Error retrieving document: {str(e)}")
        return jsonify({'error': 'Failed to retrieve document'}), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error."""
    return jsonify({'error': 'File too large'}), 413

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
