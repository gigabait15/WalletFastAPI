from fastapi import FastAPI
from config import settings
from database import engine
from wallet.models import Wallet
from wallet import routers

app = FastAPI()


@app.on_event("startup")
async def startup():
    """
    Событие запуска приложения. Создает таблицы в базе данных, если их нет.
    """
    settings.create_database()

    async with engine.begin() as conn:
        await conn.run_sync(Wallet.metadata.create_all)


app.include_router(routers.router, prefix="/api/v1")
