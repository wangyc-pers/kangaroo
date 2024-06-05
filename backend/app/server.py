import logging

from app.api.router import api_router
from app.common.logger import configure_logging
from app.common.redis import init_redis_pool
from app.common.resp import SUCCESS
from app.config import settings
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI

log = logging.getLogger(__name__)


def create_app() -> FastAPI:

    app = FastAPI(
        on_startup=[app_startup],
        on_shutdown=[app_shutdown],
    )

    # Middleware
    app.add_middleware(CorrelationIdMiddleware)

    @app.get("/")
    def read_root():
        log.info("ping pong")
        return SUCCESS(data={"ping": "pong"})

    # add api router
    app.include_router(api_router)
    return app


def app_startup():
    log.info("startup app")
    configure_logging(path=settings.LOG_FILE, debug=settings.DEBUG)
    if settings.REDIS_URL:
        init_redis_pool(str(settings.REDIS_URL))


def app_shutdown():
    log.info("shutdown app")
