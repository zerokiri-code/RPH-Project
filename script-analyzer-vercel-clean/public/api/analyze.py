import os
import requests
from flask import Request, jsonify
from dotenv import load_dotenv

load_dotenv()

def handler(request: Request):
    if request.method != 'POST':
        return jsonify({"error": "Only POST allowed"}), 405

    script = request.form.get('script', '')
    prompt = f"Analyze this script. Identify cliché plot points and suggest improvements:\n\n{script}"

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
        return jsonify({"analysis": analysis})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
