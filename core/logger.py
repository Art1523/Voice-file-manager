"""Logging helpers for VoiceFileManager."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

_LOGGER_CONFIGURED = False


def configure_logging() -> None:
    """Configure the shared application logger once."""

    global _LOGGER_CONFIGURED

    if _LOGGER_CONFIGURED:
        return

    project_root = Path(__file__).resolve().parent.parent
    logs_dir = project_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    log_file = logs_dir / "voicefilemanager.log"

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(
        logging.Formatter("%(levelname)s | %(name)s | %(message)s")
    )

    root_logger.handlers.clear()
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    _LOGGER_CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    """Return a logger after ensuring logging is configured."""

    configure_logging()
    return logging.getLogger(name)
