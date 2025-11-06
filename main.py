from fastapi import FastAPI
from src.api.endpoints import router
from src.core.database import check_db_connection, init_db, get_session
from src.core.spimex_data import generate_fake_data


app = FastAPI(title="SPIMEX Microservice", version="1.0.0")


@app.on_event("startup")
async def startup_event():

    await check_db_connection()

    await init_db()

    async for session in get_session():
        await generate_fake_data(session)

app.include_router(router)