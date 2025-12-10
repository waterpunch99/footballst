import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE_PATH = os.path.join(LOG_DIR, "pipeline.log")


LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


file_handler = RotatingFileHandler(
    LOG_FILE_PATH,
    maxBytes=5 * 1024 * 1024,  
    backupCount=3,
    encoding="utf-8",
)

stream_handler = logging.StreamHandler()

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[file_handler, stream_handler]
)

logger = logging.getLogger("footballst")
