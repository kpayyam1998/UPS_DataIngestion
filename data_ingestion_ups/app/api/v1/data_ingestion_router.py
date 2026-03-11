from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from services.vector_service import VectorService, GenerateResponse
from schemas.vector_schema import QueryRequest
from core.logger import logger
from utils.file_manager import FileManager


router = APIRouter(
    prefix="/vector",
    tags=["Vector Operations"]
)


def get_vector_service():
    return VectorService()


def get_generate_service():
    return GenerateResponse()


def get_file_manager():
    return FileManager()


###############################################################
# Document Ingestion
###############################################################
@router.post("/ingest", status_code=status.HTTP_200_OK)
async def ingest_documents(
    file: UploadFile = File(...),
    service: VectorService = Depends(get_vector_service),
    file_manager: FileManager = Depends(get_file_manager)
):

    file_path = None
    try:

        logger.info(f"Uploading file: {file.filename}")
        file_bytes = await file.read()
        file_path = file_manager.save_uploaded_file(file_bytes, file.filename)
        count = service.ingest(file_path)
        file_manager.move_to_completed(file_path)
        return {
            "message": "Ingestion completed",
            "documents_ingested": count
        }

    except Exception:
        logger.exception("Document ingestion failed")
        if file_path:
            file_manager.move_to_failed(file_path)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ingestion failed"
        )


###############################################################
# Vector Search
###############################################################
@router.post("/search", status_code=status.HTTP_200_OK)
async def search_documents(
    payload: QueryRequest,
    service: VectorService = Depends(get_vector_service)
):

    try:
        logger.info(f"Search query received: {payload.query}")
        results = service.search(payload.query)

        return {
            "query": payload.query,
            "results": results
        }

    except Exception:
        logger.exception("Vector search failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Vector search failed"
        )


###############################################################
# Generate Response with help of vectordb
###############################################################
@router.post("/generate_response", status_code=status.HTTP_200_OK)
async def generate_response(
    payload: QueryRequest,
    service: GenerateResponse = Depends(get_generate_service)
):

    try:
        logger.info(f"Generating response for query: {payload.query}")
        response = service.generate_response(payload.query)

        return {
            "query": payload.query,
            "response": response
        }

    except Exception:
        logger.exception("Response generation failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Response generation failed"
        )