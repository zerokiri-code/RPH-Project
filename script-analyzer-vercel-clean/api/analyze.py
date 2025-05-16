import os
import tempfile
import requests
from flask import Request, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

# Libraries for parsing different files
from io import BytesIO

# Install PyPDF2 and python-docx in requirements.txt (add these)
import PyPDF2
import docx

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file_stream):
    reader = PyPDF2.PdfReader(file_stream)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file_stream):
    document = docx.Document(file_stream)
    text = "\n".join([para.text for para in document.paragraphs])
    return text

def handler(request: Request):
    if request.method != 'POST':
        return jsonify({"error": "Only POST allowed"}), 405

    if 'file' not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": f"Unsupported file extension. Allowed: {ALLOWED_EXTENSIONS}"}), 400

    filename = secure_filename(file.filename)
    extracted_text = ""

    try:
        ext = filename.rsplit('.', 1)[1].lower()
        if ext == 'txt':
            extracted_text = file.read().decode('utf-8', errors='ignore')
        elif ext == 'pdf':
            extracted_text = extract_text_from_pdf(file)
        elif ext in ('doc', 'docx'):
            extracted_text = extract_text_from_docx(file)
        else:
            return jsonify({"error": "Unsupported file type"}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to extract text: {str(e)}"}), 500

    prompt = f"Analyze this script. Identify cliché plot points and suggest improvements:\n\n{extracted_text}"

    headers = {
        'Authorization': f'Bearer {os.getenv("OPENROUTER_API_KEY")}',
        'Content-Type': 'application/json'
    }

    payload = {
        "model": "meta-llama/llama-3.3-8b-instruct:free",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        r = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        data = r.json()
        analysis = data.get("choices", [{}])[0].get("message", {}).get("content", "No response.")
        return jsonify({"analysis": analysis, "extracted_text": extracted_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
