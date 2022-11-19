import asyncio

import sentry_sdk
import structlog_sentry_logger
import uvicorn

from OpenDebates.config import config, config_schema

# Faster Event Loop
try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

# Validate Config
config_schema.validate(config)


# Logging Config
UVICORN_LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(message)s",
            "use_colors": None,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
        },
    },
    "loggers": {
        "uvicorn": {"level": "INFO"},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"level": "INFO", "propagate": False},
    },
}

sentry_sdk.init(config["api"]["sentry"], traces_sample_rate=1.0)
logger = structlog_sentry_logger.get_logger()


def main():
    uvicorn.run(
        "OpenDebates.app:app",
        host="127.0.0.1",
        port=5000,
        log_config=UVICORN_LOGGING_CONFIG,
        log_level=config["api"]["log_level"].lower(),
    )


if __name__ == "__main__":
    main()
