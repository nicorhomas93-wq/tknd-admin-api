from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse

app = FastAPI(title="TKND Admin API")

# CORS, falls ein Frontend zugreift (Domains anpassen)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # produktiv: spezifische Domains eintragen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
def root():
    # entweder JSON-Status …
    return JSONResponse({"service": "tknd-admin-api", "status": "ok"})
    # … oder auf die Swagger-UI:
    # return RedirectResponse(url="/docs")

@app.get("/health", include_in_schema=False)
def health():
    return {"status": "ok"}
