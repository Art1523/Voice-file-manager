"""Application configuration management."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULT_CONFIG = {
    "theme": "dark",
    "voice": "default",
    "speech_speed": 170,
    "microphone": 0,
    "default_folders": [],
    "recent_folders": [],
    "search_roots": [],
    "preferred_apps": {
        "chrome": "chrome",
        "vscode": "code",
        "calculator": "calc",
        "paint": "mspaint",
        "notepad": "notepad",
        "explorer": "explorer",
        "cmd": "cmd",
        "powershell": "powershell",
        "spotify": "spotify",
        "task manager": "taskmgr",
    },
}


class AppConfig:
    """Store and persist user preferences in JSON."""

    def __init__(self, path: Path | None = None):
        self.project_root = Path(__file__).resolve().parent.parent
        self.path = path or self.project_root / "assets" / "config.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load()

    def _load(self) -> dict[str, Any]:
        if not self.path.exists():
            self._save(DEFAULT_CONFIG)
            return dict(DEFAULT_CONFIG)

        try:
            with self.path.open("r", encoding="utf-8") as file_handle:
                data = json.load(file_handle)
        except (OSError, json.JSONDecodeError):
            data = {}

        merged = dict(DEFAULT_CONFIG)
        merged.update(data)
        merged["preferred_apps"] = {
            **DEFAULT_CONFIG["preferred_apps"],
            **data.get("preferred_apps", {}),
        }
        self._save(merged)
        return merged

    def _save(self, data: dict[str, Any]) -> None:
        with self.path.open("w", encoding="utf-8") as file_handle:
            json.dump(data, file_handle, indent=2, ensure_ascii=False)

    def save(self) -> None:
        self._save(self.data)

    def reload(self) -> None:
        self.data = self._load()

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.data[key] = value
        self.save()

    def add_recent_folder(self, folder_path: str) -> None:
        recent_folders = self.data.setdefault("recent_folders", [])
        if folder_path in recent_folders:
            recent_folders.remove(folder_path)
        recent_folders.insert(0, folder_path)
        self.data["recent_folders"] = recent_folders[:10]
        self.save()
