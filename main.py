# main.py — TKND Admin API (vollständig, kopierfertig)

# Optional für lokale Entwicklung: .env laden (in Render NICHT erforderlich)
try:
    from dotenv import load_dotenv  # nur lokal benötigt
    load_dotenv()
except Exception:
    # Wenn python-dotenv nicht installiert ist, einfach ignorieren
    pass

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Router-Imports
from routers.auth import auth_router
from routers.admins import admins_router
from routers.customers import customers_router
from routers.technicians import technicians_router

# DB-Setup: Modelle importieren und Tabellen einmalig erstellen
from core.database import Base, engine
import models.user  # registriert das User-Model
import models.ticket  # registriert das Ticket-Model

# ---------------------------
# App erstellen & konfigurieren
# ---------------------------
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "https://tknd-unity-gbr.com").split(",")

app = FastAPI(title="TKND Admin API")

# CORS: für Cookies/Session muss allow_credentials=True gesetzt sein
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,     # z. B. ["https://tknd-unity-gbr.com"]
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# ---------------------------
# DB-Schema einmalig erstellen
# ---------------------------
# WICHTIG: passiert hier zentral, nicht in den Routern,
# damit keine Zirkular-Imports entstehen.
Base.metadata.create_all(bind=engine)

# ---------------------------
# Health-Check (für Render)
# ---------------------------
@app.get("/", include_in_schema=False)
def health():
    return {"service": "tknd-admin-api", "status": "ok"}

# ---------------------------
# Router registrieren
# ---------------------------
app.include_router(auth_router,         prefix="/auth",        tags=["auth"])
app.include_router(admins_router,       prefix="/admins",      tags=["admins"])
app.include_router(customers_router,    prefix="/customers",   tags=["customers"])
app.include_router(technicians_router,  prefix="/technicians", tags=["technicians"])
