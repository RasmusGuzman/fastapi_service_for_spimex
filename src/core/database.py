from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import logging

from src.core.settings import settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(filename)s:%(lineno)d: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


engine = create_async_engine(settings.DB_DSN, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def check_db_connection():
    try:
        logger.info("Проверяем подключение к БД...")
        async with engine.connect():
            logger.info("Подключение к БД успешно")
    except Exception as e:
        logger.error(f"Ошибка подключения к БД: {str(e)}")
        raise


async def init_db():
    try:
        async with engine.begin() as conn:
            try:
                await conn.run_sync(Base.metadata.create_all)
                logger.info("База данных успешно инициализиорвана")
            except Exception as e:
                logger.error(f"Ошибка SQLAlchemy DBAPI: {str(e)}")
                raise
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise

async def get_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()