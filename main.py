from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from routers import auth as auth_router
from routers import users as users_router

app = FastAPI(title="TKND Admin API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # produktiv: explizite Domains eintragen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
def root():
    return JSONResponse({"service": "tknd-admin-api", "status": "ok"})

@app.get("/health", include_in_schema=False)
def health():
    return {"status": "ok"}

app.include_router(auth_router.router)
app.include_router(users_router.router)

# (optional) Admin-Panel:
# import admin  # falls du sqladmin verwenden möchtest
