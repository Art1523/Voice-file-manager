"""Global file search with cached indexing."""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

from core.app_config import AppConfig
from core.logger import get_logger

logger = get_logger(__name__)


@dataclass(slots=True)
class SearchResult:
    name: str
    path: str
    is_dir: bool


class FileSearchIndex:
    """Build and reuse an index over common user folders."""

    def __init__(self, cache_path: Path | None = None):
        self.project_root = Path(__file__).resolve().parent.parent
        self.cache_path = cache_path or self.project_root / "assets" / "search_index.json"
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self._index: list[SearchResult] | None = None
        self._config = AppConfig()

    def _default_roots(self) -> list[Path]:
        self._config.reload()
        home = Path.home()
        candidate_roots = [
            home / "Desktop",
            home / "Downloads",
            home / "Documents",
            home / "Pictures",
            home / "Videos",
            home / "Music",
        ]
        configured_roots = [Path(item) for item in self._config.get("search_roots", []) if item]
        candidate_roots.extend(configured_roots)
        return [root for root in candidate_roots if root.exists()]

    def _load_cache(self) -> list[SearchResult]:
        if not self.cache_path.exists():
            return []

        try:
            with self.cache_path.open("r", encoding="utf-8") as file_handle:
                raw_results = json.load(file_handle)
        except (OSError, json.JSONDecodeError):
            return []

        results: list[SearchResult] = []
        for item in raw_results:
            try:
                results.append(SearchResult(**item))
            except TypeError:
                continue
        return results

    def _save_cache(self, results: list[SearchResult]) -> None:
        with self.cache_path.open("w", encoding="utf-8") as file_handle:
            json.dump([asdict(item) for item in results], file_handle, indent=2, ensure_ascii=False)

    def _walk_root(self, root: Path) -> Iterable[SearchResult]:
        for path in root.rglob("*"):
            try:
                yield SearchResult(path.name, str(path), path.is_dir())
            except OSError:
                continue

    def build_index(self, refresh: bool = False) -> list[SearchResult]:
        if self._index is not None and not refresh:
            return self._index

        cached_results = self._load_cache()
        if cached_results and not refresh:
            self._index = cached_results
            return cached_results

        results: list[SearchResult] = []
        for root in self._default_roots():
            try:
                results.extend(self._walk_root(root))
            except (OSError, PermissionError):
                logger.warning("Skipping root during indexing: %s", root)

        self._index = results
        self._save_cache(results)
        return results

    def search(self, query: str, limit: int = 20) -> list[SearchResult]:
        normalized_query = query.strip().lower()
        if not normalized_query:
            return []

        results = self.build_index()
        ranked: list[tuple[int, SearchResult]] = []

        for item in results:
            candidate = f"{item.name} {item.path}".lower()
            if normalized_query == item.name.lower():
                rank = 0
            elif candidate.startswith(normalized_query):
                rank = 1
            elif normalized_query in candidate:
                rank = 2
            else:
                continue
            ranked.append((rank, item))

        ranked.sort(key=lambda entry: (entry[0], entry[1].name.lower()))
        return [item for _, item in ranked[:limit]]
