from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from core.database import get_db, Base, engine
from core.security import hash_password, verify_password, create_access_token
from schemas.user import LoginRequest, RegisterRequest, UserOut
from models.user import User, RoleEnum
from core.config import settings
import os

auth_router = APIRouter()
Base.metadata.create_all(bind=engine)

@auth_router.post("/register", response_model=UserOut)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    if req.role not in (RoleEnum.CUSTOMER, RoleEnum.TECHNICIAN):
        raise HTTPException(status_code=400, detail="Only CUSTOMER or TECHNICIAN allowed")
    if db.query(User).filter(User.email == req.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    u = User(email=req.email, display_name=req.display_name,
             hashed_password=hash_password(req.password), role=req.role)
    db.add(u); db.commit(); db.refresh(u)
    return u

@auth_router.post("/login")
def login(req: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(subject=user.email)
    response.set_cookie(
        key="access_token", value=token,
        max_age=60*settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        httponly=True, secure=settings.COOKIE_SECURE,
        samesite="Lax", domain=settings.COOKIE_DOMAIN, path="/",
    )
    return {"ok": True, "role": user.role}

@auth_router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token", path="/", domain=settings.COOKIE_DOMAIN)
    return {"ok": True}

@auth_router.get("/me", response_model=UserOut)
def me(current: User = Depends(...)):  # setze hier deine get_current_user()-Dependency aus deps/auth_cookie.py
    return current

@auth_router.post("/bootstrap", include_in_schema=False)
def bootstrap(db: Session = Depends(get_db)):
    email = os.getenv("SUPERADMIN_EMAIL"); password = os.getenv("SUPERADMIN_PASSWORD")
    if not email or not password:
        raise HTTPException(status_code=400, detail="SUPERADMIN_EMAIL/PASSWORD missing")
    if db.query(User).filter(User.email == email).first(): return {"message": "exists"}
    u = User(email=email, display_name="Superadmin", hashed_password=hash_password(password), role=RoleEnum.SUPERADMIN)
    db.add(u); db.commit()
    return {"message": "created"}
