import logging
from contextlib import asynccontextmanager
from typing import Callable

from fastapi import FastAPI, Request, Response

from app.api import api_router
from app.database.sql.session import init_db

logger = logging.getLogger(__name__)


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

    @app.middleware("http")
    async def log_requests(request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        logger.warning(f"{request.method} {request.url} | {response.status_code}")
        return response

    return app
