"""Tool registry for ART AI command execution."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Any

from core.logger import get_logger

logger = get_logger(__name__)

ToolHandler = Callable[[dict[str, Any]], str]


@dataclass(slots=True)
class ToolResult:
    tool_name: str
    success: bool
    output: str


class ToolRegistry:
    """Register and execute assistant tools."""

    def __init__(self):
        self._handlers: dict[str, ToolHandler] = {}

    def register(self, name: str, handler: ToolHandler) -> None:
        self._handlers[name] = handler

    def execute(self, tool_name: str, payload: dict[str, Any]) -> ToolResult:
        handler = self._handlers.get(tool_name)
        if handler is None:
            return ToolResult(tool_name, False, "Unknown command.")

        try:
            output = handler(payload)
            return ToolResult(tool_name, True, output)
        except Exception as exc:  # pragma: no cover - external IO boundary
            logger.exception("Tool execution failed: %s", tool_name)
            return ToolResult(tool_name, False, f"Error: {exc}")
