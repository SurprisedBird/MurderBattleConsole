import logging
from logging.config import fileConfig

fileConfig(fname='log_config.ini', disable_existing_loggers=False)
logger = logging.getLogger("mb_logger")
