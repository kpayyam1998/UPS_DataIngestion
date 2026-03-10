from pydantic_settings import BaseSettings

# this settings for retrieving configuration values from environment variables or .env file
class Settings(BaseSettings):

    qdrant_url: str
    gemini_api_key: str
    embedding_model: str
    collection_name: str
    vector_size: int

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()