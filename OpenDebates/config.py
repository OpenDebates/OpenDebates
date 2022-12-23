import sys
from typing import List

import toml
from schema import Or, Schema

config_schema = Schema(
    {
        "api": {"production": Or(True, False), "secret": str, "allowed_hosts": List[str]},
        "logs": {
            "level": Or(
                "DEBUG",
                "INFO",
                "WARNING",
                "ERROR",
                "CRITICAL",
            ),
            "sentry": str,
        },
        "database": {
            "name": str,
            "user": str,
            "password": str,
            "host": str,
            "port": str,
        },
    }
)

# Config Loader
try:
    config = toml.load("config.toml")
except FileNotFoundError:
    sys.exit()
