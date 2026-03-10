from pydantic import BaseModel, Field


class IngestRequest(BaseModel):
    file_path: str = Field(..., example="file path of the data ingestion pdf ")


class QueryRequest(BaseModel):
    query: str = Field(..., example="user query for vector search")
