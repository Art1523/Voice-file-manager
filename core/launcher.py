"""Application launcher utilities."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass

from core.app_config import AppConfig
from core.logger import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True, slots=True)
class LaunchResult:
    success: bool
    message: str


class AppLauncher:
    """Launch common desktop applications on Windows."""

    def __init__(self, config: AppConfig | None = None):
        self.config = config or AppConfig()

    def launch(self, app_name: str) -> LaunchResult:
        self.config.reload()
        normalized = app_name.strip().lower()
        executable = self.config.get("preferred_apps", {}).get(normalized, normalized)

        try:
            subprocess.Popen(executable, shell=True)
            logger.info("Launched application: %s", executable)
            return LaunchResult(True, f"Launched {normalized or executable}.")
        except Exception as exc:  # pragma: no cover - OS-specific launch failures
            logger.exception("Failed to launch application: %s", executable)
            return LaunchResult(False, f"Could not launch {app_name}: {exc}")
