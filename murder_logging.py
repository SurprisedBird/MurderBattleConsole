import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Save logs in file
file_handler = logging.FileHandler('test_log')
file_handler.setLevel(logging.DEBUG)

# Send logging output to streams
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

# То determine log output style
formatter = logging.Formatter(
    '%(levelname)s -  %(asctime)s - %(name)s -%(funcName)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Comment line below to turn off file saving
logger.addHandler(file_handler)

# Comment line below to turn off stream output
logger.addHandler(stream_handler)
