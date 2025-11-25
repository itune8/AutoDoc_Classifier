# AutoDoc Classifier

**AutoDoc Classifier** is an intelligent document processing system that automatically classifies uploaded documents and extracts structured data from various document types. Built with Python, it provides a modular architecture for document ingestion, classification, and field extraction.

## 🚀 Features

- **Automatic Document Classification**: Identifies document types including invoices, purchase orders, paystubs, ID documents, and flood forms
- **Intelligent Field Extraction**: Extracts key fields specific to each document type using pattern matching and NLP
- **SQLite Database Storage**: Stores both raw document content and extracted structured data
- **Web Interface**: Simple web UI for document upload and processing (via `app/web.py`)
- **CLI Support**: Command-line interface for batch processing
- **Modular Architecture**: Easy to extend with new document types and extractors

## 📋 Supported Document Types

- **Invoices** - Extract vendor info, amounts, dates, line items
- **Purchase Orders** - Extract PO numbers, vendors, items, pricing
- **Paystubs** - Extract employee info, pay periods, earnings, deductions
- **ID Documents** - Extract names, DOB, ID numbers, addresses
- **Flood Forms** - Extract property info, coverage details, policy data

## 🛠️ Tech Stack

- **Python 3.9+** - Core language
- **pdfplumber** - PDF text extraction
- **SQLite3** - Database for document storage
- **Flask/FastAPI** - Web interface (optional)
- **Pattern matching & Regex** - Field extraction logic

## 📁 Project Structure

```
AutoDoc_Classifier/
├── app/
│   ├── __init__.py
│   ├── __main__.py          # CLI entry point
│   ├── main.py              # Core processing logic
│   ├── web.py               # Web interface
│   ├── classifier.py        # Document type classifier
│   ├── db.py                # Database schema & operations
│   ├── ingestion.py         # Document text extraction
│   └── extractors/          # Document-specific extractors
│       ├── invoice_extractor.py
│       ├── po_extractor.py
│       ├── paystub_extractor.py
│       ├── id_extractor.py
│       └── flood_form_extractor.py
├── uploads/                 # Uploaded documents
├── requirements.txt         # Python dependencies
└── README.md
```

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.9 or higher
- pip package manager
- Virtual environment (recommended)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/<your-username>/AutoDoc_Classifier.git
cd AutoDoc_Classifier

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

## 🎯 Usage

### Streamlit Web Interface (Recommended)

Launch the interactive web application:

```bash
# Run the Streamlit app
streamlit run app/app.py

# Or use the provided script
./run_streamlit.sh
```

The app will open automatically in your browser at `http://localhost:8501`

**Features:**
- 📤 Drag-and-drop file upload
- 🔍 Real-time document classification
- 📊 Interactive statistics dashboard
- 📚 Document history viewer

### Command Line Interface

Process a single document:

```bash
python -m app path/to/document.pdf
```

Or using the main module directly:

```bash
python -m app.main path/to/document.pdf
```

### REST API

Start the Flask API server:

```bash
python -m app.api
```

API will be available at `http://localhost:5000`. Example endpoints:
- `GET /health` - Health check
- `POST /api/v1/classify` - Upload and classify document
- `GET /api/v1/documents` - List all documents

### Database Inspection

View processed documents and extracted data:

```bash
sqlite3 documents.db
```

Example queries:

```sql
-- View all processed documents
SELECT * FROM documents;

-- View extracted invoice data
SELECT * FROM invoice;

-- View extracted purchase order data
SELECT * FROM purchase_order;
```

## 🔧 Development

### Adding a New Document Type

1. **Update Classifier** (`app/classifier.py`)
   - Add classification rules for the new document type

2. **Create Extractor** (`app/extractors/your_type_extractor.py`)
   - Implement field extraction logic specific to the document type

3. **Update Database Schema** (`app/db.py`)
   - Add new table for the document type
   - Create insert helper function

4. **Integrate in Pipeline** (`app/main.py`)
   - Add processing logic for the new document type

### Running Tests

```bash
# Add your test commands here
pytest tests/
```

## 📊 Database Schema

The system uses SQLite with the following main tables:

- `documents` - Stores raw document info (id, file_path, type, text, timestamp)
- `invoice` - Invoice-specific fields
- `purchase_order` - PO-specific fields
- `paystub` - Payroll-specific fields
- `id_document` - ID card/license-specific fields
- `flood_form` - Insurance form-specific fields

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is available for educational and internal use. Please specify your license terms as needed.

## 🙋 Support

For questions or issues, please open an issue on GitHub or contact the maintainers.

---

**Built for efficient document processing and data extraction** 🚀
