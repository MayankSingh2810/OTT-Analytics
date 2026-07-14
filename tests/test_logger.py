from utils.logger import get_logger

logger = get_logger("LOGGER_TEST")

logger.info("Logger is working successfully.")
logger.warning("This is a warning.")
logger.error("This is an error.")