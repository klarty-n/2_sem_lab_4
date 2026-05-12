import logging
from pathlib import Path

log_path = Path('program.log').resolve()

logging.basicConfig(
    level=logging.INFO,
    filename=log_path,
    filemode="a",
    datefmt="%Y-%m-%d %H:%M:%S",
    format="[%(asctime)s] %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger()


def log_info(message: str) -> None:
    logger.info(message)

def log_error(message: str) -> None:
    """
    Логирует ошибки
    :param message: сообщение об ошибке
    :return: None
    """
    logger.error(message)