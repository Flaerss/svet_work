from pathlib import Path
import logging.config

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": LOGS_DIR / "bot.log",
            "encoding": "utf-8",
            "level": "INFO"
        }
    },
    "root": {
        "handlers": ["file"],
        "level": "INFO"
    }
}