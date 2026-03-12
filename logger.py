import logging
import os


def setup_logger():
    nivel = logging.DEBUG if os.getenv("FLASK_ENV") == "development" else logging.INFO

    logging.basicConfig(
        level=nivel,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    return logging.getLogger(__name__)


logger = setup_logger()
