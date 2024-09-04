import logging

import betterlogging as bl


def setup_logging():
    """Set up logging configuration for the application.

    This method initializes the logging configuration for the
    application. It sets the log level to INFO and configures a basic
    colorized log for output. The log format includes the filename, line
    number, log level, timestamp, logger name, and log message.

    """
    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting bot")
