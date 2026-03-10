from langchain_qdrant import QdrantVectorStore

from db.qdrant_client import QdrantManager
from core.config import settings
from core.logger import logger
from utils.data_ingestion_utils import DataIngestionUtils
from models.exceptions import (
    VectorInsertException,
    VectorSearchException,
    ResponseGenerationException
)

from google import genai
from google.genai import types


class VectorService:
    """
    Service responsible for document ingestion and vector search.
    """

    def __init__(self):

        logger.info("Initializing VectorService")

        try:
            self.db = QdrantManager()
            
            self.embeddings = DataIngestionUtils.get_embeddings()
            self.db.create_collection(settings.collection_name)
            self.vector_store = QdrantVectorStore(
                client=self.db.client,
                collection_name=settings.collection_name,
                embedding=self.embeddings,
            )

            logger.info("VectorService initialized successfully")

        except Exception as exc:

            logger.exception("Failed to initialize VectorService")
            raise VectorInsertException(str(exc))

    def ingest(self, file_path: str) -> int:
        """
        Load documents, generate embeddings and store them in Qdrant.
        """

        try:

            logger.info(f"Starting ingestion for file: {file_path}")
            documents = DataIngestionUtils.load_pdf(file_path)
            if not documents:
                raise VectorInsertException("No documents found to ingest")
            ids = DataIngestionUtils.generate_ids(len(documents))
            self.vector_store.add_documents(documents=documents, ids=ids)
            logger.info(f"Successfully inserted {len(documents)} documents")
            return len(documents)

        except Exception as exc:

            logger.exception("Vector ingestion failed")
            raise VectorInsertException(str(exc))

    def search(self, query: str, k: int = 5):
        """
        Perform similarity search from Qdrant.
        """

        try:
            logger.info(f"Performing similarity search for query: {query}")
            results = self.vector_store.similarity_search(query, k=k)
            return [doc.page_content for doc in results]

        except Exception as exc:
            logger.exception("Vector search failed")
            raise VectorSearchException(str(exc))


class GenerateResponse:
    """
    Service responsible for generating responses using Gemini
    with retrieved vector context.
    """

    def __init__(self):

        logger.info("Initializing GenerateResponse service")

        try:

            self.collection_name = settings.collection_name
            self.db = QdrantManager()
            self.embeddings = DataIngestionUtils.get_embeddings()
            self.vector_store = QdrantVectorStore(
                client=self.db.client,
                collection_name=self.collection_name,
                embedding=self.embeddings,
            )
            self.genai_client = genai.Client(
                api_key=settings.gemini_api_key,
                vertexai=True
            )

            logger.info("GenerateResponse service initialized successfully")

        except Exception as exc:
            logger.exception("Failed to initialize GenerateResponse")
            raise ResponseGenerationException(str(exc))

    def retrieve_context(self, user_query: str, k: int = 5):
        """
        Retrieve relevant context from vector DB.
        """

        try:

            logger.info(f"Retrieving context for query: {user_query}")
            results = self.vector_store.similarity_search(user_query, k=k)
            context = [doc.page_content for doc in results]
            logger.info(f"Retrieved {len(context)} context documents")

            return context

        except Exception as exc:

            logger.exception("Context retrieval failed")

            raise VectorSearchException(str(exc))

    def generate_response(self, user_query: str):
        """
        Generate LLM response using retrieved vector context.
        """

        try:
            context = self.retrieve_context(user_query)
            logger.info("Generating response from Gemini")

            response = self.genai_client.models.generate_content(
                model="gemini-2.5-flash",
                config=types.GenerateContentConfig(
                    system_instruction=f"""
                    Answer the user's question using the context below.
                    Context:
                    {context}

                    If the answer is not in the context, say you don't know.
                    """,
                    temperature=0.2,
                ),
                contents=user_query,
            )
            logger.info("Response generated successfully")

            return response.text

        except Exception as exc:
            logger.exception("Response generation failed")
            raise ResponseGenerationException(str(exc))