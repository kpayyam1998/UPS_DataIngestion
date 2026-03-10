from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from core.config import settings
from core.logger import logger


class QdrantManager:

    def __init__(self):
        self.client = QdrantClient(url=settings.qdrant_url) 

    def create_collection(self,collection_name):
        """_summary_

        Args:
            collection_name (str): name of the collection to be created

        Returns:
            it will return the Qdrant client
        """
        try:
            if collection_name not in self.client.get_collections().collections:
                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(
                        size=settings.vector_size,
                        distance=Distance.COSINE
                    )
                )
                return self.client
            else:
                logger.info(f"Collection {settings.collection_name} already exists.")
                return False

            
        except Exception as e:
            pass