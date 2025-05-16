# Script Analyzer Vercel Deployment

This project is a Flask + Python app to analyze scripts for cliché plot points using OpenRouter LLM.

## Setup

1. Clone the repo.

2. Set your OpenRouter API key in Vercel environment variables as `OPENROUTER_API_KEY`.

3. Deploy to Vercel with:

```
vercel --prod
```

4. Visit your deployed app URL.

## Structure

- `index.py` – Flask app entry point
- `api/analyze.py` – API route for analysis
- `api/download.py` – API route for ZIP download
- `templates/index.html` – Frontend HTML
- `public/style.css` – Stylesheet
- `vercel.json` – Vercel config
- `requirements.txt` – Python dependencies

## Notes

- Use POST requests for API endpoints.
- The UI lets you paste scripts, analyze, and download ZIPs with original + suggestions.
