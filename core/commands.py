"""Intent detection for natural-language commands."""

from __future__ import annotations

APP_LAUNCH_KEYWORDS = {
    "chrome",
    "vscode",
    "calculator",
    "paint",
    "notepad",
    "explorer",
    "cmd",
    "powershell",
    "spotify",
    "task manager",
}

SEARCH_PREFIXES = ("search for ", "search ", "find ", "look for ")
LAUNCH_PREFIXES = ("launch ", "start ", "run ")


def detect_intent(command):

    command = command.lower().strip()
    command = " ".join(command.split())

    if not command:
        return {"intent": "unknown"}

    if command in {"exit", "quit", "close app"}:
        return {"intent": "exit"}

    if command == "current directory":
        return {"intent": "pwd"}

    if command.startswith("list files"):
        return {"intent": "list_files"}

    if command.startswith("create folder "):
        return {"intent": "create_folder", "target": command.removeprefix("create folder ").strip()}

    if command.startswith("open "):
        target = command.removeprefix("open ").strip()
        if target in APP_LAUNCH_KEYWORDS:
            return {"intent": "open_app", "target": target}
        return {"intent": "open", "target": target}

    for prefix in LAUNCH_PREFIXES:
        if command.startswith(prefix):
            target = command.removeprefix(prefix).strip()
            return {"intent": "open_app", "target": target}

    for prefix in SEARCH_PREFIXES:
        if command.startswith(prefix):
            target = command.removeprefix(prefix).strip()
            return {"intent": "search", "target": target}

    return {"intent": "unknown"}