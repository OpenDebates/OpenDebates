from logging import config
from structlog_sentry_logger import get_config_dict


__version__ = "0.1.0"

dict_config = get_config_dict()
config.dictConfig(dict_config)
