"""Assistant orchestration helpers."""

from __future__ import annotations

from core import commands
from core import file_manager
from core.conversation_memory import ConversationMemory
from core.history import HistoryManager
from core.logger import get_logger
from core.tool_registry import ToolRegistry
from core import speaker
from core import speech

logger = get_logger(__name__)
history = HistoryManager()
memory = ConversationMemory()
tool_registry = ToolRegistry()


for tool_name in ("pwd", "list_files", "create_folder", "open", "open_app", "search", "exit"):
    tool_registry.register(tool_name, file_manager.execute)


def _is_successful_result(result: str) -> bool:
    failure_markers = (
        "Unknown command.",
        "File or Folder not found.",
        "Could not launch",
        "Error:",
    )
    return not result.startswith(failure_markers)


def handle_command(command: str, source: str = "voice"):
    """Process a recognized command and return the spoken result.

    The logic is shared by the CLI entry point and the GUI so command
    handling stays in one place.
    """

    normalized_command = command.strip().lower()

    if normalized_command == "":
        return "", ""

    memory.remember("user", normalized_command, source)

    if normalized_command == "exit":
        result = "Goodbye!"
        history.record(normalized_command, "exit", result, True, source)
        memory.remember("assistant", result, source)
        speaker.speak(result)
        return normalized_command, result

    try:
        intent = commands.detect_intent(normalized_command)
        tool_name = intent.get("intent", "unknown")
        tool_result = tool_registry.execute(tool_name, intent)
        result = tool_result.output
        success = tool_result.success and _is_successful_result(result)
        history.record(normalized_command, tool_name, result, success, source)
        memory.remember("assistant", result, source)
        logger.info("Command processed: %s | %s", normalized_command, result)
    except Exception as exc:  # pragma: no cover - safety net around external IO
        result = f"Error: {exc}"
        history.record(normalized_command, "unknown", result, False, source)
        memory.remember("assistant", result, source)
        logger.exception("Command processing failed: %s", normalized_command)

    speaker.speak(result)

    return normalized_command, result


def process_voice():
    """Capture voice input, process it, and return the outcome."""

    command = speech.listen()
    return handle_command(command, source="voice")


def process_text(command: str):
    """Process a typed command using the same backend flow as voice input."""

    return handle_command(command, source="text")