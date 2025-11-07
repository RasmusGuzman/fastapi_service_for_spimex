import pytest
from freezegun import freeze_time
from dateutil import parser
from datetime import datetime, timedelta

from .conftest import API_URLS



@pytest.mark.asyncio
async def test_last_trading_dates(ac):
    count = 5
    response = await ac.get(f"{API_URLS['last_trading_dates']}{count}")
    assert response.status_code == 200
    data = response.json()
    assert "dates" in data
    for date_str in data["dates"]:
        try:
            parsed = parser.isoparse(date_str)
            assert parsed is not None
        except (ValueError, OverflowError) as e:
            pytest.fail(f"Невалидная дата '{date_str}': {e}")

@pytest.mark.asyncio
async def test_trading_results(ac, populate_db):
    response = await ac.get(API_URLS["root"])
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for item in data:
        assert "date" in item
        assert "volume" in item
        assert "total" in item


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

@pytest.mark.asyncio
@freeze_time("2025-10-01")
async def test_dynamics_invalid_dates(ac, populate_db):

    params = {
        "start_date": "invalid",
        "end_date": "2025-10-01"
    }
    response = await ac.get(API_URLS["dynamics"], params=params)

    assert response.status_code == 422


@pytest.mark.asyncio
@freeze_time("2025-10-01")
async def test_dynamics_2(ac, populate_db):
    start_date = datetime(2025, 9, 1)
    end_date = datetime(2025, 10, 1)

    params = {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
    }

    response = await ac.get(API_URLS["dynamics"], params=params)

    assert response.status_code == 200
    data = response.json()

    assert len(data) > 0, "Ответ пуст"

    for item in data:
        assert "date" in item
        assert isinstance(item["date"], str)
        try:
            parser.isoparse(item["date"])
        except Exception:
            pytest.fail(f"Невалидная дата: {item['date']}")

        assert "volume" in item
        assert isinstance(item["volume"], (int, float))
        assert item["volume"] >= 0

        assert "total" in item
        assert isinstance(item["total"], (int, float))
        assert item["total"] >= 0


@pytest.mark.asyncio
@freeze_time("2025-10-01")
async def test_filtered_trading_results(ac, populate_db):
    params = {"oil_id": "111111111111111"}
    response = await ac.get(API_URLS["trading_results"], params=params)

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0
