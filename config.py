from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration de l'application"""
    
    # Application
    app_env: str = "development"
    debug: bool = True
    secret_key: str = "change-me-in-production-09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    
    # JWT Authentication
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Neo4j
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "testpassword"
    
    # Embeddings
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_dimension: int = 384
    
    # Paiement
    payment_api_key: str = ""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


# Instance globale des settings
settings = Settings()
