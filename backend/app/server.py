import logging

from app.api.router import api_router
from app.config import settings
from app.core.logger import configure_logging
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from app.core.resp import SUCCESS

log = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        on_startup=(
            configure_logging(path=settings.LOG_FILE, debug=settings.DEBUG),
        )

    )
    app.add_middleware(CorrelationIdMiddleware)

    @app.get("/")
    def read_root():
        log.info("ping pong")
        return SUCCESS(data={"ping": "pong"})

    # add api router
    app.include_router(api_router)
    return app

