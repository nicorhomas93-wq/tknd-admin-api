from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from deps.auth_cookie import require_role
from models.user import User, RoleEnum
from schemas.user import RegisterRequest, UserOut
from core.security import hash_password

admins_router = APIRouter()

@admins_router.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), current=Depends(require_role(RoleEnum.ADMIN))):
    return db.query(User).order_by(User.id.desc()).limit(200).all()

@admins_router.post("/users", response_model=UserOut)
def create_user(req: RegisterRequest, db: Session = Depends(get_db), current=Depends(require_role(RoleEnum.ADMIN))):
    if req.role == RoleEnum.SUPERADMIN:
        raise HTTPException(status_code=403, detail="SUPERADMIN creation not allowed here")
    if req.role == RoleEnum.ADMIN:
        admin_count = db.query(User).filter(User.role == RoleEnum.ADMIN).count()
        if admin_count >= 3:
            raise HTTPException(status_code=400, detail="Max 3 admins reached")
    if db.query(User).filter(User.email == req.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    u = User(email=req.email, display_name=req.display_name,
             hashed_password=hash_password(req.password), role=req.role)
    db.add(u); db.commit(); db.refresh(u)
    return u
