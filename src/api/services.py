from typing import Dict, Any, List
from sqlalchemy.sql.expression import select, distinct, desc, and_
from datetime import datetime, timedelta

from .schemas import TradingResultSchema
from src.core.models import TradingResult
from src.core.database import get_session, logger



async def get_data() -> list[TradingResultSchema]:
    async for session in get_session():
        stmt = select(TradingResult).limit(100)
        result = await session.execute(stmt)
        rows = result.scalars().fetchall()
        return [TradingResultSchema.model_validate(row) for row in rows]


async def fetch_last_trading_dates(count: int) -> List[datetime]:
    async for session in get_session():
        check_date = datetime.now() - timedelta(days=count)
        stmt = select(TradingResult.date).where(TradingResult.date >= check_date).distinct().order_by(desc(TradingResult.date))
        result = await session.execute(stmt)
        return [row[0] for row in result.fetchall()]


async def fetch_dynamics(
    start_date: datetime,
    end_date: datetime,
    filters: Dict[str, Any],
) -> List[TradingResultSchema]:
    async for session in get_session():
        base_query = select(TradingResult).where(TradingResult.date.between(start_date, end_date)).order_by(desc(TradingResult.date))
        conditions = []
        for field, value in filters.items():
            if hasattr(TradingResult, field):
                logger.info(f"Adding condition: {field} = {value}")
                conditions.append(getattr(TradingResult, field) == value)

        final_stmt = base_query.filter(and_(*conditions)) if conditions else base_query
        logger.info(f"Final query: {final_stmt}")
        result = await session.execute(final_stmt)
        rows = result.scalars().fetchall()

        return [TradingResultSchema.model_validate(row) for row in rows]


async def fetch_recent_trades(filters: Dict[str, Any]) -> List[TradingResultSchema]:
    async for session in get_session():
        base_query = select(TradingResult).order_by(desc(TradingResult.date))
        conditions = []
        for field, value in filters.items():
            if hasattr(TradingResult, field):
                conditions.append(getattr(TradingResult, field) == value)

        final_stmt = base_query.filter(and_(*conditions)) if conditions else base_query
        result = await session.execute(final_stmt)
        rows = result.scalars().fetchall()
        return [TradingResultSchema.model_validate(row) for row in rows]