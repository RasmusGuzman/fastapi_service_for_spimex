import asyncio
from datetime import datetime
import random
from faker import Faker

from .models import TradingResult


fake = Faker('ru_RU')


async def generate_fake_data(session):
    result = []
    for _ in range(500):
        trading_result = dict(
            exchange_product_id=str(fake.uuid4()),
            exchange_product_name=f"{fake.word()}-{fake.random_int(min=100, max=999)}",
            oil_id=str(fake.uuid4()),
            delivery_basis_id=str(fake.uuid4()),
            delivery_basis_name=fake.city(),
            delivery_type_id=str(fake.uuid4()),
            volume=round(random.uniform(1000, 10000), 2),
            total=round(random.uniform(1000000, 10000000), 2),
            count=random.randint(1, 100),
            date=fake.date_time_between(start_date="-1y", end_date="now"),
            created_on=datetime.utcnow(),
            updated_on=datetime.utcnow()
        )
        result.append(trading_result)
    try:
        await session.execute(TradingResult.__table__.insert().values(result))
        await session.commit()
        print("Фиктивные записи успешно созданы.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        await session.rollback()

