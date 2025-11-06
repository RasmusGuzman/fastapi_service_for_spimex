import pytest
from datetime import datetime, timedelta

def test_sanity_check():
    assert True


@pytest.mark.asyncio
async def test_last_trading_dates(ac):
    response = await ac.get("/last-trading-dates/5")
    assert response.status_code == 200
    data = response.json()
    for date in data["dates"]:
        assert isinstance(date, str)
        datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")

@pytest.mark.asyncio
async def test_dynamics(ac, populate_db):
    start_date = datetime.now() - timedelta(days=30)
    end_date = datetime.now()
    response = await ac.get(f"/dynamics/?start_date={start_date.isoformat()}&end_date={end_date.isoformat()}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for item in data:
        assert "date" in item
        assert "volume" in item
        assert "total" in item

@pytest.mark.asyncio
async def test_trading_results(ac, populate_db):
    response = await ac.get("/trading-results/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for item in data:
        assert "date" in item
        assert "volume" in item
        assert "total" in item

@pytest.mark.asyncio
async def test_filtered_trading_results(ac, populate_db):
    response = await ac.get("/trading-results/?oil_id=some_oil_id")
    assert response.status_code == 200
    data = response.json()
    assert data == []

@pytest.mark.asyncio
async def test_root(ac, populate_db):
    response = await ac.get("/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 100
    for item in data:
        assert "date" in item
        assert "volume" in item
        assert "total" in item