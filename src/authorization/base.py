from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["Authorization"]
)

@router.post("/")
async def register_new_user(data: str):
    return {
        "status": "success",
        "data": data,
        "details": None
    }

@router.get("/")
async def authorize_new_user(data: str):
    return {
        "status": "success",
        "data": data,
        "details": None
    }