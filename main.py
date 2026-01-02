from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from routers.auth import auth_router
from routers.admins import admins_router
from routers.customers import customers_router
from routers.technicians import technicians_router

ALLOWED = os.getenv("ALLOWED_ORIGINS", "https://tknd-unity-gbr.com").split(",")

app = FastAPI(title="TKND Admin API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
def health():
    return {"service": "tknd-admin-api", "status": "ok"}

# Router registrieren
app.include_router(auth_router,         prefix="/auth",        tags=["auth"])
app.include_router(admins_router,       prefix="/admins",      tags=["admins"])
app.include_router(customers_router,    prefix="/customers",   tags=["customers"])
app.include_router(technicians_router,  prefix="/technicians", tags=["technicians"])
