import logging


def setup_logging(log_file='app.log', level=logging.INFO) -> logging.Logger:
    """Set up logging configuration."""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    logger.info("Logging is set up.")
    return logger

logger = setup_logging()