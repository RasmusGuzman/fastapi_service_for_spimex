from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_DSN: str = "postgresql+asyncpg://postgres:postgres@db:5432/spimex"
    REDIS_URL: str = "redis://redis:6379"
    CACHE_TTL: int = 86400  # Время жизни кеша в секундах (сутки)

settings = Settings()