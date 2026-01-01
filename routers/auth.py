from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from .. import models, schemas
from ..security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from .deps import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=schemas.UserOut, status_code=201)
def register(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == payload.email).first():
        raise HTTPException(400, "Email bereits vergeben")
    user = models.User(
        email=payload.email,
        username=payload.username,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return schemas.UserOut(
        id=str(user.id), email=user.email, username=user.username,
        is_active=user.is_active, is_superuser=user.is_superuser
    )

@router.post("/login", response_model=schemas.TokenPair)
def login(payload: schemas.UserCreate, request: Request, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash) or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access = create_access_token(str(user.id))
    refresh, jti, exp = create_refresh_token(str(user.id))
    db.add(models.RefreshToken(jti=jti, user_id=user.id, expires_at=exp,
                               user_agent=request.headers.get("User-Agent"),
                               ip_hash=request.client.host))
    user.last_login_at = datetime.utcnow()
    db.commit()
    return {"access_token": access, "refresh_token": refresh}

@router.post("/refresh", response_model=schemas.TokenPair)
def refresh_token(refresh_token: str, request: Request, db: Session = Depends(get_db)):
    try:
        data = decode_token(refresh_token)
        if data.get("type") != "refresh":
            raise ValueError("wrong type")
    except Exception:
        raise HTTPException(401, "Invalid refresh token")

    jti = data.get("jti")
    rt = db.get(models.RefreshToken, uuid.UUID(jti))
    if not rt or rt.revoked_at is not None or rt.expires_at < datetime.utcnow():
        raise HTTPException(401, "Refresh token revoked/expired")
    access = create_access_token(data["sub"])
    new_refresh, new_jti, new_exp = create_refresh_token(data["sub"])
    rt.revoked_at = datetime.utcnow()
    db.add(models.RefreshToken(jti=new_jti, user_id=rt.user_id, expires_at=new_exp,
                               user_agent=request.headers.get("User-Agent"),
                               ip_hash=request.client.host))
    db.commit()
    return {"access_token": access, "refresh_token": new_refresh}

@router.post("/logout")
def logout(refresh_token: str, db: Session = Depends(get_db)):
    try:
        data = decode_token(refresh_token)
        if data.get("type") != "refresh":
            raise ValueError
    except Exception:
        raise HTTPException(401, "Invalid refresh token")

    rt = db.get(models.RefreshToken, uuid.UUID(data["jti"]))
    if rt and rt.revoked_at is None:
        rt.revoked_at = datetime.utcnow()
        db.commit()
    return {"status": "ok"}
