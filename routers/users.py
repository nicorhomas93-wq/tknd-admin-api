from fastapi import APIRouter, Depends
from .deps import get_current_user, get_current_admin
from .. import models
from ..db import SessionLocal

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
def me(user = Depends(get_current_user)):
    return user

@router.get("/", dependencies=[Depends(get_current_admin)])
def list_users():
    db = SessionLocal()
    try:
        return db.query(models.User).all()
    finally:
        db.close()
