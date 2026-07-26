from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_root():
    return {"message": "Fraudscreen API is running!"}

@router.get("/health")
async def health_check():
    return {"status": "healthy"}
