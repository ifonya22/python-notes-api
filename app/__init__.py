from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import api_router
from app.config import get_logger
from app.database.sql.session import init_db

logger = get_logger()


def get_app_prod():
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        try:
            logger.info("Инициализация базы данных")
            await init_db()
            logger.info("База данных инициализирована")
        except Exception as e:
            logger.error(f"Ошибка при старте приложения {e}")
            raise
        yield

    app = FastAPI(lifespan=lifespan)
    app.include_router(api_router)

    return app
