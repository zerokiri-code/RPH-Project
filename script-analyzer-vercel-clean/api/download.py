from flask import Request, send_file
from io import BytesIO
from zipfile import ZipFile

def handler(request: Request):
    if request.method != 'POST':
        return "Only POST allowed", 405

    script = request.form.get("script", "")
    analysis = request.form.get("analysis", "")

    buffer = BytesIO()
    with ZipFile(buffer, 'w') as zipf:
        zipf.writestr("original_script.txt", script)
        zipf.writestr("suggestions.txt", analysis)

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="script_analysis.zip", mimetype="application/zip")
