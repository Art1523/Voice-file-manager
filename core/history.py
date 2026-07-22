"""Command history persistence."""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class HistoryEntry:
    timestamp: str
    command: str
    intent: str
    result: str
    success: bool
    source: str


class HistoryManager:
    """Persist and retrieve command history entries."""

    def __init__(self, path: Path | None = None):
        self.project_root = Path(__file__).resolve().parent.parent
        self.path = path or self.project_root / "assets" / "history.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._entries: list[HistoryEntry] = self._load()

    def _load(self) -> list[HistoryEntry]:
        if not self.path.exists():
            self._save([])
            return []

        try:
            with self.path.open("r", encoding="utf-8") as file_handle:
                raw_entries: list[dict[str, Any]] = json.load(file_handle)
        except (OSError, json.JSONDecodeError):
            raw_entries = []

        entries: list[HistoryEntry] = []
        for raw_entry in raw_entries:
            try:
                entries.append(HistoryEntry(**raw_entry))
            except TypeError:
                continue
        return entries

    def _save(self, entries: list[HistoryEntry]) -> None:
        with self.path.open("w", encoding="utf-8") as file_handle:
            json.dump([asdict(entry) for entry in entries], file_handle, indent=2, ensure_ascii=False)

    def record(self, command: str, intent: str, result: str, success: bool, source: str) -> HistoryEntry:
        entry = HistoryEntry(
            timestamp=datetime.now().isoformat(timespec="seconds"),
            command=command,
            intent=intent,
            result=result,
            success=success,
            source=source,
        )
        self._entries.insert(0, entry)
        self._entries = self._entries[:500]
        self._save(self._entries)
        return entry

    def latest(self, limit: int = 20) -> list[HistoryEntry]:
        return self._entries[:limit]

    def clear(self) -> None:
        self._entries = []
        self._save(self._entries)
