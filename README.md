# AI Concrete Mix Optimizer

A Streamlit app that designs concrete mixes per IS 10262:2019 with clean civil-themed UI, interactive Plotly charts, and optional Gemini AI tips.

## Quick Start (Local)
- Install Python 3.10+.
- Create and activate a virtual environment.
- Install: `pip install -r requirements.txt`.
- Run: `python -m streamlit run app.py`.

## Deploy (Streamlit Community Cloud)
- Push this folder to a public GitHub repo.
- Go to `https://share.streamlit.io/` and sign in with GitHub.
- Click “New app”, pick your repo, branch `main`, and file path `app.py`.
- Add secret in “Settings → Secrets”: set `GEMINI_API_KEY` if you want AI tips.
- App goes live on a public URL immediately.

Notes:
- `.streamlit/secrets.toml` is ignored by Git via `.gitignore`. Manage secrets in Streamlit Cloud UI.
- `requirements.txt` pins compatible versions for Cloud deployment.

## Optional: Deploy on Hugging Face Spaces
- Create a new Space (type: `Streamlit`).
- Upload `app.py` and `requirements.txt`.
- Set `GEMINI_API_KEY` in Space Secrets.
- The Space will build and host the app publicly.

## Optional: Deploy on Render/Railway
- Create a new Web Service.
- Build command: `pip install -r requirements.txt`.
- Start command: `streamlit run app.py --server.port $PORT --server.headless true`.
- Set env `PORT` (host provides) and `GEMINI_API_KEY` as needed.

## Project Structure
- `app.py` — Streamlit app.
- `requirements.txt` — dependencies.
- `.streamlit/secrets.toml` — local dev secrets (ignored in Git).
- `.gitignore` — excludes secrets and common artifacts.

## Troubleshooting
- Blank page on Cloud: check `requirements.txt` and that `app.py` is selected.
- AI tips disabled: set `GEMINI_API_KEY` in Cloud secrets.
- Graphics look off: use the sidebar Dark Theme toggle for darker environments.