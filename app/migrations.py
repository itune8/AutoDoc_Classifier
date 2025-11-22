"""
Database migration utilities for AutoDoc Classifier.
"""
import sqlite3
from pathlib import Path
from datetime import datetime
from app.config import DATABASE_PATH
from app.logger import get_logger

logger = get_logger(__name__)

MIGRATIONS = [
    {
        'version': 1,
        'name': 'initial_schema',
        'description': 'Create initial database schema',
        'sql': '''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL,
                document_type TEXT NOT NULL,
                text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        '''
    },
    {
        'version': 2,
        'name': 'add_hash_column',
        'description': 'Add file hash column to documents',
        'sql': '''
            ALTER TABLE documents ADD COLUMN file_hash TEXT;
        '''
    },
    {
        'version': 3,
        'name': 'add_metadata_table',
        'description': 'Create metadata tracking table',
        'sql': '''
            CREATE TABLE IF NOT EXISTS document_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER NOT NULL,
                key TEXT NOT NULL,
                value TEXT,
                FOREIGN KEY (document_id) REFERENCES documents(id)
            );
        '''
    },
]

def get_schema_version(conn):
    """Get current schema version from database."""
    try:
        cursor = conn.execute(
            "SELECT version FROM schema_version ORDER BY version DESC LIMIT 1"
        )
        row = cursor.fetchone()
        return row[0] if row else 0
    except sqlite3.OperationalError:
        # schema_version table doesn't exist yet
        return 0

def create_schema_version_table(conn):
    """Create schema version tracking table."""
    conn.execute('''
        CREATE TABLE IF NOT EXISTS schema_version (
            version INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()

def apply_migration(conn, migration):
    """Apply a single migration."""
    version = migration['version']
    name = migration['name']
    
    logger.info(f"Applying migration {version}: {name}")
    
    try:
        conn.executescript(migration['sql'])
        conn.execute(
            "INSERT INTO schema_version (version, name) VALUES (?, ?)",
            (version, name)
        )
        conn.commit()
        logger.info(f"Successfully applied migration {version}")
    except Exception as e:
        logger.error(f"Failed to apply migration {version}: {str(e)}")
        conn.rollback()
        raise

def run_migrations():
    """Run all pending migrations."""
    logger.info("Starting database migrations")
    
    conn = sqlite3.connect(DATABASE_PATH)
    create_schema_version_table(conn)
    
    current_version = get_schema_version(conn)
    logger.info(f"Current schema version: {current_version}")
    
    pending_migrations = [m for m in MIGRATIONS if m['version'] > current_version]
    
    if not pending_migrations:
        logger.info("No pending migrations")
        conn.close()
        return
    
    logger.info(f"Found {len(pending_migrations)} pending migrations")
    
    for migration in pending_migrations:
        apply_migration(conn, migration)
    
    conn.close()
    logger.info("All migrations completed successfully")
