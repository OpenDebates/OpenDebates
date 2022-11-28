from typing import Optional

from beanie import PydanticObjectId
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
)
from fastapi_users.authentication.strategy import AccessTokenDatabase, DatabaseStrategy
from fastapi_users_db_beanie import BeanieUserDatabase, ObjectIDIDMixin
from fastapi_users_db_beanie.access_token import (
    BeanieBaseAccessToken,
    BeanieAccessTokenDatabase,
)
from loguru import logger

from OpenDebates.config import config
from OpenDebates.db import User, get_user_db

# Secret Key
secret = config["api"]["secret"]


class UserManager(ObjectIDIDMixin, BaseUserManager[User, PydanticObjectId]):
    reset_password_token_secret = secret
    verification_token_secret = secret

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        logger.info(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        logger.info(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        logger.info(
            f"Verification requested for user {user.id}. Verification token: {token}"
        )


async def get_user_manager(user_db: BeanieUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


# Auth Configuration
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


# Access Token Configuration
class AccessToken(BeanieBaseAccessToken[PydanticObjectId]):
    pass


async def get_access_token_db():
    yield BeanieAccessTokenDatabase(AccessToken)


def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(access_token_db, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="persistent_bearer_token",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)


fastapi_users = FastAPIUsers[User, PydanticObjectId](get_user_manager, [auth_backend])
current_active_user = fastapi_users.current_user(active=True)
