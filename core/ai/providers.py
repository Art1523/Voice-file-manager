"""Provider abstractions for future local AI integrations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@dataclass(slots=True)
class AIMessage:
    role: str
    content: str


@dataclass(slots=True)
class ProviderResponse:
    text: str
    tool_name: str | None = None
    tool_payload: dict | None = None


@runtime_checkable
class AIProvider(Protocol):
    name: str

    def generate(self, messages: list[AIMessage]) -> ProviderResponse: ...

    def supports_tools(self) -> bool: ...
