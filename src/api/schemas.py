from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class TradingResultSchema(BaseModel):
    """
    Модель для представления результатов торгов.
    """
    exchange_product_id: Optional[str] = None
    exchange_product_name: Optional[str] = None
    oil_id: Optional[str] = None
    delivery_basis_id: Optional[str] = None
    delivery_basis_name: Optional[str] = None
    delivery_type_id: Optional[str] = None
    volume: Optional[float] = None
    total: Optional[float] = None
    count: Optional[int] = None
    date: Optional[datetime] = None
    created_on: Optional[datetime] = None
    updated_on: Optional[datetime] = None
    class Config:
        from_attributes = True  # Используем метаданные моделей SQLAlchemy


class DatesResponse(BaseModel):
    dates: List[datetime]