import logging
from ..core.config import settings

log = logging.getLogger(__name__)

logging.basicConfig(
    level=(LEVEL := settings.logging.log_level_value),
    format=(FORMAT := settings.logging.log_format),
)

file_handler = logging.FileHandler('backend/app.log')
file_handler.setLevel(LEVEL)
file_handler.setFormatter(logging.Formatter(FORMAT))


log.handlers = [file_handler]