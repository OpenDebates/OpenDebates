import sys

import toml
from schema import Or, Schema

config_schema = Schema(
    {
        "api": {
            "debug": Or(True, False),
            "log_level": Or(
                "DEBUG",
                "INFO",
                "WARNING",
                "ERROR",
                "CRITICAL",
            ),
            "sentry": str,
        }
    }
)

# Config Loader
try:
    config = toml.load("config.toml")
except FileNotFoundError:
    sys.exit()

# Validate Config
config_schema.validate(config)
