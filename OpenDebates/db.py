from beanie import PydanticObjectId
from fastapi_users_db_beanie import BeanieBaseUser, BeanieUserDatabase
from motor.motor_asyncio import AsyncIOMotorClient

from OpenDebates.config import config

# Database Configuration
database_uri = config["database"]["uri"]
client = AsyncIOMotorClient(database_uri, uuidRepresentation="standard")
db = client["opendebates"]


class User(BeanieBaseUser[PydanticObjectId]):
    pass


async def get_user_db():
    yield BeanieUserDatabase(User)
