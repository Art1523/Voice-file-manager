"""Plugin loading hooks for ART AI."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from core.logger import get_logger

logger = get_logger(__name__)


@dataclass(slots=True)
class PluginInfo:
    name: str
    version: str
    description: str


class AssistantPlugin(Protocol):
    def register(self, registry) -> None: ...


class PluginManager:
    """Future plugin loader for tools, providers, and UI extensions."""

    def __init__(self, plugins_path: Path | None = None):
        self.project_root = Path(__file__).resolve().parent.parent
        self.plugins_path = plugins_path or self.project_root / "plugins"
        self.plugins_path.mkdir(parents=True, exist_ok=True)
        self.loaded_plugins: list[PluginInfo] = []

    def discover(self) -> list[Path]:
        return sorted(self.plugins_path.glob("*.py"))

    def load_all(self, registry) -> list[PluginInfo]:
        # Plugin import/loading is intentionally deferred until real plugin files exist.
        logger.info("Plugin discovery ready: %s", self.plugins_path)
        return self.loaded_plugins
