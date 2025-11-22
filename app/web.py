from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from flask import Flask, render_template_string, request

from app.ingestion import extract_text_from_file
from app.classifier import classify_document
from app.extractors.invoice_extractor import extract_invoice_fields
from app.extractors.po_extractor import extract_po_fields
from app.extractors.id_extractor import (
    extract_driver_license_fields,
    extract_passport_fields,
    extract_w2_fields,
)
from app.extractors.paystub_extractor import extract_pay_stub_fields
from app.extractors.flood_form_extractor import extract_flood_form_fields
from app.db import init_db, insert_document

app = Flask(__name__)

TABLE: Dict[int, Dict[str, Any]] = {}


TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>Document Classification & Key Field Extraction</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
        }
        .container {
            width: 70%;
            margin: 40px auto;
            background-color: #ffffff;
            border: 1px solid #cccccc;
            padding: 30px;
            box-shadow: 0 0 5px rgba(0,0,0,0.1);
        }
        h2 {
            text-align: center;
            margin-top: 0;
            margin-bottom: 30px;
        }
        .upload-section {
            text-align: center;
            margin-bottom: 30px;
        }
        .upload-section input[type="file"] {
            padding: 5px 10px;
            border: 1px solid #999;
            border-radius: 3px;
        }
        .upload-section button {
            padding: 6px 18px;
            margin-left: 10px;
            border: 1px solid #4a90e2;
            background-color: #4a90e2;
            color: white;
            border-radius: 3px;
            cursor: pointer;
        }
        .upload-section button:hover {
            background-color: #3b7bc0;
        }
        h3 {
            margin-top: 10px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }
        th, td {
            border: 1px solid #cccccc;
            padding: 8px 10px;
            font-size: 14px;
        }
        th {
            background-color: #f0f0f0;
            text-align: left;
        }
        td {
            background-color: #ffffff;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Document Classification &amp; Key Field Extraction</h2>
        <div class="upload-section">
            <form method="post" enctype="multipart/form-data">
                <input type="file" name="document" required>
                <button type="submit">Upload</button>
            </form>
        </div>

        <h3>Response</h3>
        <table>
            <tr>
                <th>sno</th>
                <th>name_of_document</th>
                <th>type_of_document</th>
                <th>key_fields</th>
                <th>datetime</th>
            </tr>
            {% for idx, row in rows.items() %}
            <tr>
                <td>{{ idx }}</td>
                <td>{{ row.name }}</td>
                <td>{{ row.type }}</td>
                <td>{{ row.fields }}</td>
                <td>{{ row.dt }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
</body>
</html>"""


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("document")
        if file:
            filename = file.filename
            save_path = Path("uploads") / filename
            save_path.parent.mkdir(exist_ok=True)
            file.save(save_path)

            text = extract_text_from_file(str(save_path))
            print("===== DEBUG EXTRACTED TEXT (first 500 chars) from", filename)
            print(text[:500])
            doc_type = classify_document(text)

            # Only store base document for now
            insert_document(str(save_path), doc_type, text)

            if doc_type == "invoice":
                fields = extract_invoice_fields(text)
            elif doc_type == "purchase_order":
                fields = extract_po_fields(text)
            elif doc_type == "driver_license":
                fields = extract_driver_license_fields(text)
            elif doc_type == "passport":
                fields = extract_passport_fields(text)
            elif doc_type == "w2":
                fields = extract_w2_fields(text)
            elif doc_type == "pay_stub":
                fields = extract_pay_stub_fields(text)
            elif doc_type == "flood_form":
                fields = extract_flood_form_fields(text)
            else:
                fields = {}

            idx = len(TABLE) + 1
            TABLE[idx] = {
                "name": filename,
                "type": doc_type,
                "fields": str(fields),
                "dt": datetime.now().strftime("%m/%d/%Y %H:%M:%S"),
            }

    return render_template_string(TEMPLATE, rows=TABLE)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
