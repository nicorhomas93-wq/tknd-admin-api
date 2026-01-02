# routers/auth.py (Auszug)
from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.orm import Session

from deps.auth_cookie import get_current_user        # ← hier importieren
from models.user import User

auth_router = APIRouter()

@auth_router.get("/me")
def me(current: User = Depends(get_current_user)):
    return current
