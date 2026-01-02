from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Direkte Datei-Importe:
from routers.users import router as users_router
from routers.auth import auth_router

app = FastAPI(title="TKND Admin API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In Produktion: spezifische Domains eintragen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
async def health():
    return {"service": "tknd-admin-api", "status": "ok"}

@app.get("/health", include_in_schema=False)
async def health2():
    return JSONResponse({"status": "ok"})

# Router einbinden
app.include_router(users_router)
app.include_router(auth_router)
