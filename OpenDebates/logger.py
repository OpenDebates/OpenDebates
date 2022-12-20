import logging
import sys

import sentry_sdk
from loguru import logger
from sentry_sdk.integrations.logging import (
    LoggingIntegration,
    BreadcrumbHandler,
    EventHandler,
)

from OpenDebates.config import config

LOG_LEVEL = config["logs"]["level"]


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists.
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )
