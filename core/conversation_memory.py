"""Conversation memory persistence for ART AI."""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class MemoryItem:
    timestamp: str
    role: str
    content: str
    source: str


class ConversationMemory:
    """Keep a rolling record of recent conversations and commands."""

    def __init__(self, path: Path | None = None):
        self.project_root = Path(__file__).resolve().parent.parent
        self.path = path or self.project_root / "assets" / "conversation_memory.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._items: list[MemoryItem] = self._load()

    def _load(self) -> list[MemoryItem]:
        if not self.path.exists():
            self._save([])
            return []

        try:
            with self.path.open("r", encoding="utf-8") as file_handle:
                raw_items: list[dict[str, Any]] = json.load(file_handle)
        except (OSError, json.JSONDecodeError):
            raw_items = []

        items: list[MemoryItem] = []
        for raw_item in raw_items:
            try:
                items.append(MemoryItem(**raw_item))
            except TypeError:
                continue
        return items

    def _save(self, items: list[MemoryItem]) -> None:
        with self.path.open("w", encoding="utf-8") as file_handle:
            json.dump([asdict(item) for item in items], file_handle, indent=2, ensure_ascii=False)

    def remember(self, role: str, content: str, source: str) -> MemoryItem:
        item = MemoryItem(
            timestamp=datetime.now().isoformat(timespec="seconds"),
            role=role,
            content=content,
            source=source,
        )
        self._items.append(item)
        self._items = self._items[-2000:]
        self._save(self._items)
        return item

    def recent(self, limit: int = 20) -> list[MemoryItem]:
        return self._items[-limit:]

    def clear(self) -> None:
        self._items = []
        self._save(self._items)
