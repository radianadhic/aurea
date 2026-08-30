"""Application configuration via pydantic-settings."""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    # Service
    VERSION: str = "1.0.0"
    ENV: str = "dev"
    SERVICE_NAME: str = "mdm-ml-service"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8087
    WORKERS: int = 4

    # CORS
    CORS_ORIGINS: list[str] = ["*"]

    # PostgreSQL
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "mdm_ml"
    DB_USER: str = "mdm"
    DB_PASSWORD: str = "mdm123"
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""
    REDIS_DB: int = 0
    CACHE_TTL: int = 3600  # 1 hour

    # Kafka
    KAFKA_BOOTSTRAP: str = "localhost:9092"
    KAFKA_CONSUMER_GROUP: str = "ml-service"
    KAFKA_TOPIC_CUSTOMER_EVENTS: str = "mdm.customer.events"
    KAFKA_TOPIC_TRANSACTION_EVENTS: str = "mdm.transaction.events"

    # JWT
    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_AUDIENCE: str = "mdm-steward-ui"

    # ML Models
    MODEL_DIR: str = "/app/models"
    CHURN_MODEL_PATH: str = "models/churn_v1.joblib"
    RISK_MODEL_PATH: str = "models/risk_v1.joblib"
    SEGMENT_MODEL_PATH: str = "models/segment_v1.joblib"
    ANOMALY_MODEL_PATH: str = "models/anomaly_v1.joblib"
    CLV_MODEL_PATH: str = "models/clv_v1.joblib"

    # Feature flags
    USE_GPU: bool = False
    PREDICTION_BATCH_SIZE: int = 1000
    ANOMALY_THRESHOLD: float = 0.85

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def sync_database_url(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
