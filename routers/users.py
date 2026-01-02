from fastapi import APIRouter

# In users.py heißt der Router 'router' – passt zum Import oben
router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
async def list_users():
    return [{"id": 1, "name": "Alice"}]
