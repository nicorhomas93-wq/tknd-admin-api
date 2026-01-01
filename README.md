# TKND Admin API
ECHO ist ausgeschaltet (OFF).
API fuer Admin-Funktionen, bereitgestellt als Web Service auf **Render**.
ECHO ist ausgeschaltet (OFF).
## Quickstart
- **Lokal**:
```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```
ECHO ist ausgeschaltet (OFF).
- **Render**:
 1. New > Web Service > Repo: `nichothomas93-wq/tknd-admin-api`
 2. Build: `pip install -r requirements.txt`
 3. Start: `gunicorn main:app --workers 4 --bind 0.0.0.0:$PORT`
ECHO ist ausgeschaltet (OFF).
Ausfuehrliche Anleitung: [docs/render.md](docs/renderecho
## Healthcheck
`GET /` gibt:
```json
{ "status": "ok", "service": "tknd-admin-api" }
```
ECHO ist ausgeschaltet (OFF).
## Hinweise
- Stelle sicher, dass keine Secrets im Code sind. Verwende Environment Variablen in Render.
- Fuer FastAPI/ASGI kann auch folgender StartCommand verwendet werden:
  `gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:$PORT`
