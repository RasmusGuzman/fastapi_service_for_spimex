import pytest_asyncio
import asyncio
from httpx import AsyncClient, ASGITransport
from main import app
from src.core.database import Base, get_session
from src.core.database_for_tests import test_engine, TestingSessionLocal
from src.core.spimex_data import generate_fake_data


API_URLS = {
    "last_trading_dates": "/last-trading-dates/",
    "dynamics": "/dynamics/",
    "trading_results": "/trading-results/",
    "root": "/",
}


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(autouse=True, scope="module")
def _override_get_session():
    async def _get_test_session():
        async with TestingSessionLocal() as session:
            yield session
    app.dependency_overrides[get_session] = _get_test_session

@pytest_asyncio.fixture(scope="module", autouse=True)
async def prepare_database(event_loop):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def async_session():
    async with TestingSessionLocal() as session:
        yield session

@pytest_asyncio.fixture()
async def ac():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest_asyncio.fixture(autouse=True)
async def populate_db(async_session):
    await generate_fake_data(async_session)
    yield

@pytest_asyncio.fixture(scope="function")
def fixture_with_request(request):
    print(f"Фикстура вызвана для теста: {request.node.name}")
    yield
    print(f"Фикстура завершена для теста: {request.node.name}")


