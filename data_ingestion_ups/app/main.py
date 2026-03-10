from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.data_ingestion_router import data_ingestion_router
from api.v1.health_check_rounter import health_router

app = FastAPI(title="UPS Vector Ingestion Service")
# CORS configuration

# CORS configuration
origins = [
    "*",   # allow all (for development)
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)   


app.include_router(data_ingestion_router, prefix="/api/v1/vector")
app.include_router(health_router, prefix="/api/v1/health")