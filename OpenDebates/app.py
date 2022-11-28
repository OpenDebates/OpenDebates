import logging

import sentry_sdk
from fastapi import FastAPI
from sentry_sdk.integrations.logging import (
    LoggingIntegration,
    BreadcrumbHandler,
    EventHandler,
)

import OpenDebates
from OpenDebates.config import config
from OpenDebates.logger import logger

# Logging Config
environment = "production" if config["api"]["production"] else "development"
sentry_sdk.init(
    config["logs"]["sentry"],
    environment=environment,
    integrations=[LoggingIntegration(level=None, event_level=None)],
    traces_sample_rate=1.0,
)
logger.add(BreadcrumbHandler(level=logging.DEBUG), level=logging.DEBUG)
logger.add(EventHandler(level=logging.ERROR), level=logging.ERROR)

if environment == "production":
    logger.add(
        ".logs/{time}_access.log",
        rotation="50 MB",
        retention="15 days",
        filter="uvicorn",
        level=logging.DEBUG,
    )
    logger.add(
        ".logs/{time}_general.log",
        rotation="50 MB",
        retention="15 days",
        filter="OpenDebates",
        level=logging.INFO,
    )
else:
    logger.add(
        ".logs/{time}_access.log",
        rotation="10 MB",
        retention="2 days",
        filter="uvicorn",
        level=logging.DEBUG,
    )
    logger.add(
        ".logs/{time}_general.log",
        rotation="10 MB",
        retention="2 days",
        filter="OpenDebates",
        level=logging.INFO,
    )

# Create App Instance
logger.info(f"Starting OpenDebates: {OpenDebates.__version__}")
app = FastAPI(title="Open Debates", version=OpenDebates.__version__)
database_uri = config["database"]["uri"]
