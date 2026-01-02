# deps/auth_cookie.py
from fastapi import Depends, HTTPException, status, Cookie
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import decode_token
from models.user import User, RoleEnum

def get_current_user(db: Session = Depends(get_db), access_token: str | None = Cookie(default=None)) -> User:
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No auth cookie")
    try:
        payload = decode_token(access_token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    email = payload.get("sub")
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive or not found")
    return user

def require_role(required: RoleEnum):
    def checker(current: User = Depends(get_current_user)):
        order = {
            RoleEnum.SUPERADMIN: 4,
            RoleEnum.ADMIN: 3,
            RoleEnum.TECHNICIAN: 2,
            RoleEnum.CUSTOMER: 1,
        }
        if order[current.role] < order[required]:
            raise HTTPException(status_code=403, detail="Insufficient privileges")
        return current
    return checker
