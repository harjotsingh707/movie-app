# Movie Database App (OMDb) — Complete

This repository contains a Flask web app that searches movies & TV shows using the OMDb API.

## Run locally
1. Copy .env.example to .env and fill OMDB_API_KEY and SESSION_SECRET, or set environment variables.
2. Install deps:
   pip install -r requirements.txt
3. Run:
   python main.py

## Deploy
Recommended: Render.com or Railway. Use `gunicorn main:app` as the start command.

## Notes
- Do NOT commit real API keys to a public repo. .env is included locally only.
