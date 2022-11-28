import logging

import sentry_sdk
from beanie import init_beanie
from fastapi import FastAPI
from sentry_sdk.integrations.logging import (
    LoggingIntegration,
    BreadcrumbHandler,
    EventHandler,
)

import OpenDebates
from OpenDebates.config import config
from OpenDebates.db import User, db
from OpenDebates.logger import logger
from OpenDebates.schemas import UserRead, UserCreate, UserUpdate
from OpenDebates.users import fastapi_users, auth_backend

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


# Routers
app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Authentication"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["Authentication"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["Authentication"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["Users"],
)


@app.on_event("startup")
async def on_startup():
    await init_beanie(
        database=db,
        document_models=[
            User,
        ],
    )
