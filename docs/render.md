# Render Deployment Leitfaden - TKND Admin API
ECHO ist ausgeschaltet (OFF).
Dieser Leitfaden beschreibt die Bereitstellung von **tknd-admin-api** als *Web Service* auf Render.
ECHO ist ausgeschaltet (OFF).
## Voraussetzungen
- GitHub-Repo: https://github.com/nichothomas93-wq/tknd-admin-api
- Python 3.x
- Dateien: `main.py`, `requirements.txt`, `.gitignore`, `render.yaml`
ECHO ist ausgeschaltet (OFF).
## Schritt-fuer-Schritt (Render Dashboard)
1. Melde dich an auf https://render.com
3. Verbinde dein Repo: `nichothomas93-wq/tknd-admin-api`
4. Einstellung:
   - **Environment**: Python
   - **Region/Plan**: nach Bedarf (Free zum Testen)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn main:app --workers 4 --bind 0.0.0.0:$PORT`
5. **Create Web Service** klicken und Build abwarten.
6. Teste die Live-URL: `GET /` sollte `{ "status": "ok", "service": "tknd-admin-api" }` liefern.
ECHO ist ausgeschaltet (OFF).
## Umgebungsvariablen (optional)
  - `ENV=production`
  - `API_KEY=...`
  - `DATABASE_URL=...`
ECHO ist ausgeschaltet (OFF).
## Wartung / Updates
- Aenderungen committen und pushen: Render triggert einen neuen Build automatisch.
ECHO ist ausgeschaltet (OFF).
## Troubleshooting
- **Build scheitert**: Pruefe `requirements.txt` und Python-Version.
- **Port-Fehler**: Stelle sicher, dass `main.py` den `PORT` aus ENV nutzt.
- **Timeouts/Bad Gateway**: Ueberpruefe den `startCommand` (gunicorn) und App-Importpfad.
- **Unauthorized Git Pull**: Pruefe Repo-Sichtbarkeit oder Render-Github-Verbindung neu verknuepfen.
ECHO ist ausgeschaltet (OFF).
## Lokaler Start
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
ECHO ist ausgeschaltet (OFF).
## Optional: Struktur
```
tknd-admin-api/
├─ main.py
├─ requirements.txt
├─ render.yaml
├─ README.md
└─ docs/
   └─ render.md
```
ECHO ist ausgeschaltet (OFF).
## StartCommand Erklaerung
- `gunicorn main:app` bedeutet: Modul `main`, Objekt `app` als WSGI/ASGI Entrypoint.
- `--bind 0.0.0.0:$PORT` hoert auf dem von Render bereitgestellten Port.
- `--workers 4` startet 4 Worker-Prozesse (fuer einfache APIs ausreichend).
ECHO ist ausgeschaltet (OFF).
## Hinweise fuer ASGI (FastAPI)
- Gunicorn nutzt standardmaessig `uvicorn.workers.UvicornWorker` fuer FastAPI:
  `gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:$PORT`
ECHO ist ausgeschaltet (OFF).
