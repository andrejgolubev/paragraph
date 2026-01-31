import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from ..core.config import settings

LOG_FORMATTER = logging.Formatter(settings.logging.log_format)

log = logging.getLogger(__name__)
log.setLevel(LOG_LEVEL := settings.logging.log_level_value)
log.propagate = False  # не дублировать на родительский handler


file_handler = RotatingFileHandler(
    Path(__file__).parent.parent / "app.log",
    maxBytes=2**20 * settings.logging.max_file_size_mb,
    backupCount=settings.logging.backup_files, 
    encoding="utf-8"
)
file_handler.setLevel(LOG_LEVEL)
file_handler.setFormatter(LOG_FORMATTER)

log.handlers = [file_handler]