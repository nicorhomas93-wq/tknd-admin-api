import os, datetime, uuid
from passlib.context import CryptContext
import jwt

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TTL = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
REFRESH_TTL_DAYS = int(os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS", "30"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)

def create_access_token(sub: str) -> str:
    now = datetime.datetime.utcnow()
    payload = {"sub": sub, "iat": now, "exp": now + datetime.timedelta(minutes=ACCESS_TTL), "type": "access"}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(sub: str, jti: uuid.UUID | None = None):
    now = datetime.datetime.utcnow()
    jti = jti or uuid.uuid4()
    exp = now + datetime.timedelta(days=REFRESH_TTL_DAYS)
    payload = {"sub": sub, "iat": now, "exp": exp, "jti": str(jti), "type": "refresh"}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token, jti, exp

def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
