from langchain_community.document_loaders import PyMuPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from uuid import uuid4

from core.config import settings
from core.logger import logger
from models.exceptions import DocumentLoadException



class DataIngestionUtils:

    @staticmethod
    def load_pdf(file_path: str):
        try:

            loader = PyMuPDFLoader(file_path)
            documents = loader.load()
            logger.info(f"Loaded {len(documents)} documents")
            return documents

        except Exception as e:
            logger.error("PDF loading failed")
            raise DocumentLoadException(str(e))

    @staticmethod
    def get_embeddings():

        return GoogleGenerativeAIEmbeddings(
            model=settings.embedding_model,
            api_key=settings.gemini_api_key,
            vertexai=True,
        )

    @staticmethod
    def generate_ids(count: int):
        return [str(uuid4()) for _ in range(count)]