import os
from fastapi import FastAPI
import uvicorn
ECHO ist ausgeschaltet (OFF).
app = FastAPI(title="TKND Admin API"
ECHO ist ausgeschaltet (OFF).
@app.get("/")
def root():
    return {"status": "ok", "service": "tknd-admin-api"}
ECHO ist ausgeschaltet (OFF).
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
