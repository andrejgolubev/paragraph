import logging
from pathlib import Path
from backend.core.config import settings

log = logging.getLogger(__name__)

logging.basicConfig(
    level=(LEVEL := settings.logging.log_level_value),
    format=(FORMAT := settings.logging.log_format),
)


log.setLevel(LEVEL) # обязательно

log_path = Path(__file__).parent.parent / "app.log"
file_handler = logging.FileHandler(log_path)
file_handler.setLevel(LEVEL)
file_handler.setFormatter(logging.Formatter(FORMAT))
file_handler.encoding = 'utf-8'

log.handlers = [file_handler]