from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database URLs (Supabase format)
    # Example: postgresql+asyncpg://postgres.xxx:password@aws-0-us-east-1.pooler.supabase.com:5432/postgres
    database_url: str = "postgresql+asyncpg://fraud_user:fraud_pass@db:5432/fraud_db"
    database_url_sync: str = "postgresql://fraud_user:fraud_pass@db:5432/fraud_db"

    # API Security
    api_key: str = "change-me-in-production"
    rate_limit_per_second: int = 100

    # Model Configuration
    model_dir: str = "models"
    fallback_amount_limit: float = 50.0
    fraud_threshold: float = 0.10  # Updated default for model v6.0

    # Logging
    log_level: str = "INFO"

    model_config = {"env_file": ".env"}


settings = Settings()
