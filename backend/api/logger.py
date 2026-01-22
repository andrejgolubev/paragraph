import logging
from pathlib import Path
from backend.core.config import settings

log = logging.getLogger(__name__)

logging.basicConfig(
    level=(LEVEL := settings.logging.log_level_value),
    format=(FORMAT := settings.logging.log_format),
)


log_path = Path(__file__).parent / "app.log"
file_handler = logging.FileHandler(log_path)
file_handler.setLevel(LEVEL)
file_handler.setFormatter(logging.Formatter(FORMAT))


log.handlers = [file_handler]