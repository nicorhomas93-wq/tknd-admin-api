from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    username: str | None = None
    password: str

class UserOut(BaseModel):
    id: str
    email: EmailStr
    username: str | None = None
    is_active: bool
    is_superuser: bool

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
