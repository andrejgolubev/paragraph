import logging
from pathlib import Path
from ..core.config import settings


LOG_FORMATTER = logging.Formatter(settings.logging.log_format)
LEVEL = settings.logging.log_level_value

log = logging.getLogger(__name__)
log.setLevel(LEVEL)
log.propagate = False  # не дублировать на родительский handler

file_handler = logging.FileHandler(
    Path(__file__).parent.parent / "app.log",
    encoding="utf-8"
)
file_handler.setLevel(LEVEL)
file_handler.setFormatter(LOG_FORMATTER)

log.handlers = [file_handler]