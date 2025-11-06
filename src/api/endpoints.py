from fastapi import APIRouter, Depends
from starlette.responses import Response
from datetime import datetime
from fastapi.responses import JSONResponse
from typing import Optional, List
from .services import fetch_last_trading_dates, fetch_dynamics, fetch_recent_trades, get_data
from .schemas import DatesResponse, TradingResultSchema
from src.core.cache import get_cache, set_cache
from src.core.database import get_session


router = APIRouter()


@router.get("/", response_model=list[TradingResultSchema], response_class=JSONResponse)
async def root(session=Depends(get_session)):
    data = await get_data(session)
    return data

@router.get("/last-trading-dates/{count}", response_model=DatesResponse)
async def get_last_trading_dates(count: int):
    key = f"last_dates_{count}"
    cached_value = await get_cache(key)
    if cached_value:
        return DatesResponse(dates=cached_value)
    dates = await fetch_last_trading_dates(count)
    await set_cache(key, dates)
    return DatesResponse(dates=dates)

@router.get("/dynamics/", response_model=List[TradingResultSchema])
async def get_dynamics(
    start_date: datetime,
    end_date: datetime,
    oil_id: Optional[str] = None,
    delivery_type_id: Optional[str] = None,
    delivery_basis_id: Optional[str] = None
):
    filters = {}
    if oil_id:
        filters["oil_id"] = oil_id
    if delivery_type_id:
        filters["delivery_type_id"] = delivery_type_id
    if delivery_basis_id:
        filters["delivery_basis_id"] = delivery_basis_id
    trades = await fetch_dynamics(start_date, end_date, filters)
    return trades

@router.get("/trading-results/", response_model=List[TradingResultSchema])
async def get_trading_results(
    oil_id: Optional[str] = None,
    delivery_type_id: Optional[str] = None,
    delivery_basis_id: Optional[str] = None
):
    filters = {}
    if oil_id:
        filters["oil_id"] = oil_id
    if delivery_type_id:
        filters["delivery_type_id"] = delivery_type_id
    if delivery_basis_id:
        filters["delivery_basis_id"] = delivery_basis_id

    trades = await fetch_recent_trades(filters)
    return trades