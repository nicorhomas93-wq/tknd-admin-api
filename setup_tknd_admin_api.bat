
@echo off
setlocal ENABLEDELAYEDEXPANSION

:: ==============================
:: Einstellungen
:: ==============================
set "GITHUB_USER=nichothomas93-wq"
set "REPO_NAME=tknd-admin-api"
set "DEFAULT_BRANCH=main"
set "REMOTE_URL=https://github.com/%GITHUB_USER%/%REPO_NAME%.git"

echo.
echo ==========================================================
echo   TKND Admin API - GitHub Setup (ohne curl) + Render-Doku
echo ==========================================================
echo.

:: ------------------------------
:: 1) Git-Check
:: ------------------------------
where git >nul 2>nul
if errorlevel 1 (
  echo [FEHLER] Git wurde nicht gefunden. Bitte installiere Git:
  echo         winget install --id Git.Git -e --source winget
  exit /b 1
)

:: ------------------------------
:: 2) Lokales Git-Repo initialisieren
:: ------------------------------
if not exist ".git" (
  git init
  echo [OK] Neues Git-Repo initialisiert.
) else (
  echo [INFO] Git-Repo existiert bereits.
)

:: ------------------------------
:: 3) Projektgrundstruktur erzeugen (nur wenn fehlt)
:: ------------------------------
if not exist ".gitignore" (
  > .gitignore echo __pycache__/
  >> .gitignore echo *.pyc
  >> .gitignore echo .env
  >> .gitignore echo .venv/
  >> .gitignore echo venv/
  >> .gitignore echo .pytest_cache/
  >> .gitignore echo .mypy_cache/
  >> .gitignore echo .DS_Store
)

if not exist "requirements.txt" (
  > requirements.txt echo fastapi==0.115.0
  >> requirements.txt echo uvicorn[standard]==0.30.0
  >> requirements.txt echo gunicorn==21.2.0
)

if not exist "main.py" (
  > main.py echo import os
  >> main.py echo from fastapi import FastAPI
  >> main.py echo import uvicorn
  >> main.py echo
  >> main.py echo app = FastAPI(title="TKND Admin API")
  >> main.py echo
  >> main.py echo @app.get("/")
  >> main.py echo def root():
  >> main.py echo ^    return {"status": "ok", "service": "tknd-admin-api"}
  >> main.py echo
  >> main.py echo if __name__ == "__main__":
  >> main.py echo ^    port = int(os.environ.get("PORT", 8000))
  >> main.py echo ^    uvicorn.run(app, host="0.0.0.0", port=port)
)

if not exist "render.yaml" (
  > render.yaml echo services:
  >> render.yaml echo ^  - type: web
  >> render.yaml echo ^    name: tknd-admin-api
  >> render.yaml echo ^    env: python
  >> render.yaml echo ^    plan: free
  >> render.yaml echo ^    buildCommand: "pip install -r requirements.txt"
  >> render.yaml echo ^    startCommand: "gunicorn main:app --workers 4 --bind 0.0.0.0:^$PORT"
)

:: ------------------------------
:: 4) Render-Dokumentation generieren
:: ------------------------------
if not exist "docs" mkdir docs

> docs/render.md echo # Render Deployment Leitfaden - TKND Admin API
>> docs/render.md echo
>> docs/render.md echo Dieser Leitfaden beschreibt die Bereitstellung von **tknd-admin-api** als *Web Service* auf Render.
>> docs/render.md echo
>> docs/render.md echo ## Voraussetzungen
>> docs/render.md echo - GitHub-Repo: https://github.com/%GITHUB_USER%/%REPO_NAME%
>> docs/render.md echo - Python 3.x
>> docs/render.md echo - Dateien: `main.py`, `requirements.txt`, `.gitignore`, `render.yaml`
>> docs/render.md echo
>> docs/render.md echo ## Schritt-fuer-Schritt (Render Dashboard)
>> docs/render.md echo 1. Melde dich an auf https://render.com
>> docs/render.md echo 2. **New -> Web Service**
>> docs/render.md echo 3. Verbinde dein Repo: `%GITHUB_USER%/%REPO_NAME%`
>> docs/render.md echo 4. Einstellung:
>> docs/render.md echo    - **Environment**: Python
>> docs/render.md echo    - **Region/Plan**: nach Bedarf (Free zum Testen)
>> docs/render.md echo    - **Build Command**: `pip install -r requirements.txt`
>> docs/render.md echo    - **Start Command**: `gunicorn main:app --workers 4 --bind 0.0.0.0:^$PORT`
>> docs/render.md echo 5. **Create Web Service** klicken und Build abwarten.
>> docs/render.md echo 6. Teste die Live-URL: `GET /` sollte `{ "status": "ok", "service": "tknd-admin-api" }` liefern.
>> docs/render.md echo
>> docs/render.md echo ## Umgebungsvariablen (optional)
>> docs/render.md echo - Ueber **Settings -> Environment** in Render setzen, z.B.:
>> docs/render.md echo   - `ENV=production`
>> docs/render.md echo   - `API_KEY=...`
>> docs/render.md echo   - `DATABASE_URL=...`
>> docs/render.md echo
>> docs/render.md echo ## Wartung / Updates
>> docs/render.md echo - Aenderungen committen und pushen: Render triggert einen neuen Build automatisch.
>> docs/render.md echo - Logs ueber **Events -> Logs** im Service ansehen.
>> docs/render.md echo
>> docs/render.md echo ## Troubleshooting
>> docs/render.md echo - **Build scheitert**: Pruefe `requirements.txt` und Python-Version.
>> docs/render.md echo - **Port-Fehler**: Stelle sicher, dass `main.py` den `PORT` aus ENV nutzt.
>> docs/render.md echo - **Timeouts/Bad Gateway**: Ueberpruefe den `startCommand` (gunicorn) und App-Importpfad.
>> docs/render.md echo - **Unauthorized Git Pull**: Pruefe Repo-Sichtbarkeit oder Render-Github-Verbindung neu verknuepfen.
>> docs/render.md echo
>> docs/render.md echo ## Lokaler Start
>> docs/render.md echo ```bash
>> docs/render.md echo uvicorn main:app --host 0.0.0.0 --port 8000
>> docs/render.md echo ```
>> docs/render.md echo
>> docs/render.md echo ## Optional: Struktur
>> docs/render.md echo ```
>> docs/render.md echo tknd-admin-api/
>> docs/render.md echo ├─ main.py
>> docs/render.md echo ├─ requirements.txt
>> docs/render.md echo ├─ render.yaml
>> docs/render.md echo ├─ README.md
>> docs/render.md echo └─ docs/
>> docs/render.md echo    └─ render.md
>> docs/render.md echo ```
>> docs/render.md echo
>> docs/render.md echo ## StartCommand Erklaerung
>> docs/render.md echo - `gunicorn main:app` bedeutet: Modul `main`, Objekt `app` als WSGI/ASGI Entrypoint.
>> docs/render.md echo - `--bind 0.0.0.0:^$PORT` hoert auf dem von Render bereitgestellten Port.
>> docs/render.md echo - `--workers 4` startet 4 Worker-Prozesse (fuer einfache APIs ausreichend).
>> docs/render.md echo
>> docs/render.md echo ## Hinweise fuer ASGI (FastAPI)
>> docs/render.md echo - Gunicorn nutzt standardmaessig `uvicorn.workers.UvicornWorker` fuer FastAPI:
>> docs/render.md echo   `gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:^$PORT`
>> docs/render.md echo

> README.md echo # TKND Admin API
>> README.md echo
>> README.md echo API fuer Admin-Funktionen, bereitgestellt als Web Service auf **Render**.
>> README.md echo
>> README.md echo ## Quickstart
>> README.md echo - **Lokal**:
>> README.md echo ```bash
>> README.md echo pip install -r requirements.txt
>> README.md echo uvicorn main:app --host 0.0.0.0 --port 8000
>> README.md echo ```
>> README.md echo
>> README.md echo - **Render**:
>> README.md echo  1. New ^> Web Service ^> Repo: `%GITHUB_USER%/%REPO_NAME%`
>> README.md echo  2. Build: `pip install -r requirements.txt`
>> README.md echo  3. Start: `gunicorn main:app --workers 4 --bind 0.0.0.0:^$PORT`
>> README.md echo
>> README.md echo Ausfuehrliche Anleitung: [docs/render.md](docs/renderecho
>> README.md echo ## Healthcheck
>> README.md echo `GET /` gibt:
>> README.md echo ```json
>> README.md echo { "status": "ok", "service": "tknd-admin-api" }
>> README.md echo ```
>> README.md echo
>> README.md echo ## Hinweise
>> README.md echo - Stelle sicher, dass keine Secrets im Code sind. Verwende Environment Variablen in Render.
>> README.md echo - Fuer FastAPI/ASGI kann auch folgender StartCommand verwendet werden:
>> README.md echo   `gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:^$PORT`

:: ------------------------------
:: 5) Commit vorbereiten
:: ------------------------------
git add -A
git commit -m "Initial commit: TKND Admin API + Render-Doku" 2>nul

:: ------------------------------
:: 6) Remote setzen
:: ------------------------------
git remote remove origin >nul 2>nul
git remote add origin %REMOTE_URL%
echo [OK] Remote gesetzt: %REMOTE_URL%

:: ------------------------------
:: 7) Branch erstellen und Push
:: ------------------------------
git branch -M %DEFAULT_BRANCH%
git push -u origin %DEFAULT_BRANCH%

echo.
echo ==========================================================
echo   Fertig! Repo ist online:
echo   %REMOTE_URL%
echo ----------------------------------------------------------
echo   Naechster Schritt (Render Dashboard):
echo   - New -> Web Service -> Repo verbinden
echo   - Build: pip install -r requirements.txt
echo   - Start: gunicorn main:app --workers 4 --bind 0.0.0.0:$PORT
echo   - Details: docs/render.md im Repo lesen
echo ==========================================================
endlocal
