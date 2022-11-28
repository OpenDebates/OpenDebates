import sys

import toml
from schema import Or, Schema

config_schema = Schema(
    {
        "api": {"production": Or(True, False)},
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
        "database": {"uri": str},
    }
)

# Config Loader
try:
    config = toml.load("config.toml")
except FileNotFoundError:
    sys.exit()
