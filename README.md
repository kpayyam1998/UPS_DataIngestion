
# UPS Data Ingestion & RAG Service

A FastAPI-based data ingestion and retrieval service that processes PDF documents,
stores embeddings in Qdrant Vector Database, and generates responses using Google Gemini models.

## Features
- PDF document ingestion
- Vector similarity search using Qdrant
- Context-aware response generation with Gemini


## Project Structure
```bash
app/
├── api/
│   └── v1/
│       ├── data_ingestion_router.py
│       └── health_check_router.py
├── core/
│   ├── config.py
│   └── logger.py
├── db/
│   └── qdrant_client.py
├── models/
│   └── exceptions.py
├── schemas/
│   └── vector_schema.py
├── services/
│   └── vector_service.py
├── utils/
│   ├── data_ingestion_utils.py
│   └── file_manager.py
├── data/
│   ├── ingestion_file/
│   ├── completed_file/
│   └── failed_file/
└── main.py
```
## Environment Variables

Create a .env file in the project root.
```bash
QDRANT_URL=http://localhost:6333
COLLECTION_NAME=test_ups_collection
VECTOR_SIZE=3072
GEMINI_API_KEY=your_api_key
EMBEDDING_MODEL=models/gemini-embedding-001
```
## Installation

1. Clone repository

```bash
git clone <repo-url>
cd data_ingestion_ups
```
2. Create virtual environment
```bash
python -m venv .venv
```

Activate:
Windows:
```bash
.venv\Scripts\activate
```


3. Install dependencies
```bash
pip install -r requirements.txt
```

## Running Qdrant
```bash
docker run -p 6333:6333 qdrant/qdrant
```

Dashboard:
```bash
http://localhost:6333/dashboard
```

## Run the API

```bash
uvicorn app.main:app --reload
```

Swagger docs:
```bash
http://127.0.0.1:8000/docs
```

## API Endpoints

### Ingest Document
```bash
POST http://localhost:8000/api/v1/vector/vector/ingest
```
```bash
Upload file (multipart form):
file=document.pdf

Response:
{
  "message": "Ingestion completed",
  "documents_ingested": 32
}
```
`

### Vector Search
```bash
POST /api/v1/vector/search

Request:
{
  "query": "UPS Business Resource Groups"
}
```
### Generate Response
```bash
POST http://localhost:8000/api/v1/vector/vector/generate_response

Request:
{
  "query": "What are UPS Business Resource Groups?"
}


Response:
{
  "query": "What are UPS Business Resource Groups?",
  "response": "generated response will be here"
}
```
# Streamlit UI RUN command
```bash
  streamlit run ui.py
```

## Future Improvements
- Store all the details in the database (ex: MongoDB)
- Background ingestion workers
- Batch embedding pipeline
- Metadata filtering
- Duplicate file detection
