from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.database import Base

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db:5432/spimex_test"

test_engine = create_async_engine(
    TEST_DATABASE_URL
)
TestingSessionLocal = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


