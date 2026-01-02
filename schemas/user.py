from pydantic import BaseModel, EmailStr
from typing import Optional
from models.user import RoleEnum

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    display_name: Optional[str] = None
    role: RoleEnum  # nur CUSTOMER oder TECHNICIAN

class UserOut(BaseModel):
    id: int
    email: EmailStr
    display_name: Optional[str] = None
    role: RoleEnum
    is_active: bool
    class Config:
        orm_mode = True
