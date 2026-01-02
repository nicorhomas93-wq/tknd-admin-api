# routers/auth.py
from fastapi import APIRouter

# Der Router heißt 'auth_router', damit der Import in main.py funktioniert
auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/check")
async def auth_check():
    # einfache gültige Rückgabe
    return {"status": "auth ok"}
