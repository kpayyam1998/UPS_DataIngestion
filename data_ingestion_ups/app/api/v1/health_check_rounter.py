from fastapi import APIRouter

# health check router 
health_router = APIRouter()

@health_router.get("/health")
async def health_check():
    return {"status": "server is healthy.....:)"}