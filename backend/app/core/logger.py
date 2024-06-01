import logging
import os
from logging.config import dictConfig

log = logging.getLogger(__name__)


def configure_logging(path, debug=True):
    dir_name = os.path.dirname(path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    level = "DEBUG" if debug else "INFO"
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "correlation_id": {
                    "()": "asgi_correlation_id.CorrelationIdFilter",
                    "uuid_length": 32,
                    "default_value": "-",
                },
            },
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                    "format": "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d [%(correlation_id)s]: %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "filters": ["correlation_id"],
                    "formatter": "console",
                },
                "file": {
                    "class": "logging.FileHandler",
                    "filename": path,
                    "formatter": "console",
                },
            },
            "loggers": {
                "root": {
                    "handlers": ["console"] if debug else ["file"],
                    "level": level,
                    "propagate": True,
                },
            },
        }
    )
