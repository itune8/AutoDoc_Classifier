import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional
from app.logger import get_logger
from app.config import DATABASE_PATH

logger = get_logger(__name__)

DB_PATH = DATABASE_PATH


def get_connection() -> sqlite3.Connection:
    """Get database connection with row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_path TEXT,
        document_type TEXT,
        raw_text TEXT
    )
    """
    )

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS invoice (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER,
        invoice_number TEXT,
        invoice_date TEXT,
        total_amount TEXT,
        vendor_name TEXT,
        FOREIGN KEY(document_id) REFERENCES documents(id)
    )
    """
    )

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS purchase_order (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER,
        po_number TEXT,
        po_date TEXT,
        total_amount TEXT,
        buyer_name TEXT,
        FOREIGN KEY(document_id) REFERENCES documents(id)
    )
    """
    )

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS driver_license (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER,
        name TEXT,
        dl_number TEXT,
        dob TEXT,
        FOREIGN KEY(document_id) REFERENCES documents(id)
    )
    """
    )

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS passport (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER,
        name TEXT,
        passport_number TEXT,
        FOREIGN KEY(document_id) REFERENCES documents(id)
    )
    """
    )

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS w2 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER,
        ssn TEXT,
        wages TEXT,
        ein TEXT,
        FOREIGN KEY(document_id) REFERENCES documents(id)
    )
    """
    )

    conn.commit()
    conn.close()


def insert_document(file_path: str, document_type: str, text: str) -> int:
    """Insert a document record and return its ID."""
    logger.info(f"Inserting document: {file_path}, type: {document_type}")
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO documents (file_path, document_type, raw_text) VALUES (?, ?, ?)",
        (file_path, document_type, text),
    )
    document_id = cur.lastrowid
    conn.commit()
    conn.close()
    
    logger.info(f"Document inserted with ID: {document_id}")
    return document_id


def get_all_documents() -> List[Dict]:
    """Get all documents from database."""
    logger.debug("Fetching all documents")
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, file_path, document_type FROM documents ORDER BY id DESC")
    
    rows = cur.fetchall()
    conn.close()
    
    documents = [dict(row) for row in rows]
    logger.debug(f"Found {len(documents)} documents")
    
    return documents


def get_document_by_id(doc_id: int) -> Optional[Dict]:
    """Get a specific document by ID."""
    logger.debug(f"Fetching document ID: {doc_id}")
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
    
    row = cur.fetchone()
    conn.close()
    
    return dict(row) if row else None


def insert_invoice(document_id: int, fields: Dict[str, Any]) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO invoice (document_id, invoice_number, invoice_date, total_amount, vendor_name)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            document_id,
            fields.get("invoice_number"),
            fields.get("invoice_date"),
            fields.get("total_amount"),
            fields.get("vendor_name"),
        ),
    )
    conn.commit()
    conn.close()


def insert_purchase_order(document_id: int, fields: Dict[str, Any]) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO purchase_order (document_id, po_number, po_date, total_amount, buyer_name)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            document_id,
            fields.get("po_number"),
            fields.get("po_date"),
            fields.get("total_amount"),
            fields.get("buyer_name"),
        ),
    )
    conn.commit()
    conn.close()


def insert_driver_license(document_id: int, fields: Dict[str, Any]) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO driver_license (document_id, name, dl_number, dob)
        VALUES (?, ?, ?, ?)
        """,
        (
            document_id,
            fields.get("name"),
            fields.get("dl_number"),
            fields.get("DOB"),
        ),
    )
    conn.commit()
    conn.close()


def insert_passport(document_id: int, fields: Dict[str, Any]) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO passport (document_id, name, passport_number)
        VALUES (?, ?, ?)
        """,
        (
            document_id,
            fields.get("name"),
            fields.get("passport_number"),
        ),
    )
    conn.commit()
    conn.close()


def insert_w2(document_id: int, fields: Dict[str, Any]) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO w2 (document_id, ssn, wages, ein)
        VALUES (?, ?, ?, ?)
        """,
        (
            document_id,
            fields.get("ssn"),
            fields.get("wages"),
            fields.get("ein"),
        ),
    )
    conn.commit()
    conn.close()
