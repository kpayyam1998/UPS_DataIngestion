from pydantic import BaseModel, Field
from typing import List

class IngestRequest(BaseModel):
    file_path: str = Field(..., example="file path of the data ingestion pdf ")


class QueryRequest(BaseModel):
    query: str = Field(..., example="user query for vector search")


class EvaluateRequest(BaseModel):
    user_query: str = Field(..., example="user query for evaluation")
    reference: str = Field(..., example="reference answer for evaluation")
    retrieved_contexts: List[str] = Field(
        ..., 
        example=["retrieved context 1", "retrieved context 2"]
    )