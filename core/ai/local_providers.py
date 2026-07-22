"""Placeholder local provider adapters for future use."""

from __future__ import annotations

from dataclasses import dataclass

from core.ai.providers import AIMessage, ProviderResponse


@dataclass(slots=True)
class OfflineProvider:
    name: str

    def generate(self, messages: list[AIMessage]) -> ProviderResponse:
        last_message = messages[-1].content if messages else ""
        return ProviderResponse(text=last_message)

    def supports_tools(self) -> bool:
        return False


class OllamaProvider(OfflineProvider):
    def __init__(self):
        super().__init__(name="ollama")


class QwenProvider(OfflineProvider):
    def __init__(self):
        super().__init__(name="qwen")


class LlamaProvider(OfflineProvider):
    def __init__(self):
        super().__init__(name="llama")


class WhisperProvider(OfflineProvider):
    def __init__(self):
        super().__init__(name="whisper")


class PiperProvider(OfflineProvider):
    def __init__(self):
        super().__init__(name="piper")
