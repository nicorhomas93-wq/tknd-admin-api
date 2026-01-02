from fastapi import APIRouter

# Der Name MUSS 'auth_router' sein, weil du ihn so importierst
auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/check")
async def auth_check():
    return {"status": "auth ok"}
``
