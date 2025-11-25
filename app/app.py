"""
Streamlit web application for AutoDoc Classifier.
"""
import streamlit as st
import os
from pathlib import Path
import tempfile
import pandas as pd
from datetime import datetime

from app.ingestion import extract_text_from_file
from app.classifier import classify_document, get_classification_confidence
from app.db import init_db, insert_document, get_all_documents
from app.utils import validate_file, calculate_file_hash
from app.logger import setup_logging, get_logger
from app.exceptions import AutoDocException
from app.config import ALLOWED_EXTENSIONS, MAX_UPLOAD_SIZE

# Setup
setup_logging()
logger = get_logger(__name__)
init_db()

# Page config
st.set_page_config(
    page_title="AutoDoc Classifier",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .doc-type {
        font-size: 1.5rem;
        font-weight: bold;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .confidence-high {
        background-color: #d4edda;
        color: #155724;
    }
    .confidence-medium {
        background-color: #fff3cd;
        color: #856404;
    }
    .confidence-low {
        background-color: #f8d7da;
        color: #721c24;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">📄 AutoDoc Classifier</h1>', unsafe_allow_html=True)
st.markdown("**Automatic Document Classification and Field Extraction System**")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.info("""
    AutoDoc Classifier automatically:
    - 📤 Accepts document uploads
    - 🔍 Extracts text from PDFs and images
    - 🏷️ Classifies document types
    - 💾 Stores results in database
    """)
    
    st.header("📊 Supported Types")
    doc_types = [
        "📝 Invoices",
        "🛒 Purchase Orders",
        "💰 Paystubs",
        "🪪 ID Documents",
        "🏠 Flood Forms",
        "📋 W2 Forms",
        "🛂 Passports"
    ]
    for doc_type in doc_types:
        st.write(f"• {doc_type}")
    
    st.header("⚙️ Settings")
    show_raw_text = st.checkbox("Show extracted text", value=False)
    auto_classify = st.checkbox("Auto-classify on upload", value=True)

# Main content tabs
tab1, tab2, tab3 = st.tabs(["📤 Upload & Classify", "📚 Document History", "📈 Statistics"])

with tab1:
    st.header("Upload Document")
    
    uploaded_file = st.file_uploader(
        "Choose a document file",
        type=['pdf', 'jpg', 'jpeg', 'png', 'bmp', 'tiff'],
        help=f"Maximum file size: {MAX_UPLOAD_SIZE / (1024*1024):.0f}MB"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        process_button = st.button("🚀 Process Document", type="primary", use_container_width=True)
    
    if uploaded_file is not None:
        # Display file info
        st.success(f"✅ File uploaded: **{uploaded_file.name}**")
        file_details = {
            "Filename": uploaded_file.name,
            "File Size": f"{uploaded_file.size / 1024:.2f} KB",
            "File Type": uploaded_file.type
        }
        
        with st.expander("📋 File Details"):
            for key, value in file_details.items():
                st.write(f"**{key}:** {value}")
        
        # Process document
        if process_button or auto_classify:
            with st.spinner("Processing document..."):
                try:
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name
                    
                    # Validate file
                    validate_file(tmp_path)
                    
                    # Extract text
                    progress_bar = st.progress(0)
                    st.text("Extracting text...")
                    progress_bar.progress(33)
                    
                    text = extract_text_from_file(tmp_path)
                    
                    # Classify
                    st.text("Classifying document...")
                    progress_bar.progress(66)
                    
                    doc_type = classify_document(text)
                    confidence = get_classification_confidence(text, doc_type)
                    
                    # Calculate hash
                    file_hash = calculate_file_hash(tmp_path)
                    
                    # Save to database
                    st.text("Saving to database...")
                    progress_bar.progress(100)
                    
                    document_id = insert_document(
                        file_path=uploaded_file.name,
                        document_type=doc_type,
                        text=text
                    )
                    
                    progress_bar.empty()
                    
                    # Display results
                    st.success("✅ Document processed successfully!")
                    
                    # Results in columns
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Document ID", f"#{document_id}")
                    
                    with col2:
                        # Confidence styling
                        if confidence >= 0.7:
                            conf_class = "confidence-high"
                        elif confidence >= 0.4:
                            conf_class = "confidence-medium"
                        else:
                            conf_class = "confidence-low"
                        
                        st.metric("Confidence", f"{confidence:.1%}")
                    
                    with col3:
                        st.metric("Text Length", f"{len(text):,} chars")
                    
                    # Document type display
                    st.markdown(f'<div class="doc-type {conf_class}">Document Type: {doc_type.upper().replace("_", " ")}</div>', 
                               unsafe_allow_html=True)
                    
                    # Show extracted text if enabled
                    if show_raw_text:
                        with st.expander("📄 Extracted Text Preview"):
                            st.text_area("Raw Text", text[:2000] + ("..." if len(text) > 2000 else ""), height=300)
                    
                    # Additional info
                    with st.expander("🔍 Additional Information"):
                        st.write(f"**File Hash (SHA256):** `{file_hash}`")
                        st.write(f"**Processing Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    # Cleanup
                    os.unlink(tmp_path)
                    
                except AutoDocException as e:
                    st.error(f"❌ Error: {str(e)}")
                    logger.error(f"Processing error: {str(e)}")
                except Exception as e:
                    st.error(f"❌ Unexpected error: {str(e)}")
                    logger.error(f"Unexpected error: {str(e)}")

with tab2:
    st.header("📚 Document History")
    
    try:
        documents = get_all_documents()
        
        if documents:
            st.write(f"**Total Documents:** {len(documents)}")
            
            # Convert to DataFrame
            df = pd.DataFrame(documents)
            
            # Display as table
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "id": "ID",
                    "file_path": "Filename",
                    "document_type": "Type",
                }
            )
            
            # Download button
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"documents_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No documents processed yet. Upload a document to get started!")
            
    except Exception as e:
        st.error(f"Error loading documents: {str(e)}")

with tab3:
    st.header("📈 Statistics")
    
    try:
        documents = get_all_documents()
        
        if documents:
            df = pd.DataFrame(documents)
            
            # Document type distribution
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Document Type Distribution")
                type_counts = df['document_type'].value_counts()
                st.bar_chart(type_counts)
            
            with col2:
                st.subheader("Statistics Summary")
                st.metric("Total Documents", len(documents))
                st.metric("Unique Types", df['document_type'].nunique())
                
                # Most common type
                if not type_counts.empty:
                    most_common = type_counts.index[0]
                    st.metric("Most Common Type", most_common.replace("_", " ").title())
            
            # Detailed breakdown
            st.subheader("Type Breakdown")
            for doc_type, count in type_counts.items():
                percentage = (count / len(documents)) * 100
                st.write(f"**{doc_type.replace('_', ' ').title()}:** {count} documents ({percentage:.1f}%)")
                st.progress(percentage / 100)
        else:
            st.info("No statistics available yet. Process some documents first!")
            
    except Exception as e:
        st.error(f"Error generating statistics: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>AutoDoc Classifier v1.0 | Built with Streamlit 🚀</p>
    </div>
    """,
    unsafe_allow_html=True
)
