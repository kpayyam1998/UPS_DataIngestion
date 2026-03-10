from fastapi import APIRouter

# health check router for monitoring the service status
health_router = APIRouter()

@health_router.get("/health")
def health_check():
    return {"status": "ok"}