"""File and application command execution."""

from __future__ import annotations

import os
from pathlib import Path

from core.app_config import AppConfig
from core.launcher import AppLauncher
from core.logger import get_logger
from core.search_index import FileSearchIndex

current_directory = Path.home()

config = AppConfig()
launcher = AppLauncher(config)
search_index = FileSearchIndex()
logger = get_logger(__name__)


def _format_directory_listing(paths):

    if not paths:
        return "Folder is empty."

    return "\n".join(paths)


def _open_item(item: Path):

    os.startfile(item)

    if item.is_dir():
        global current_directory
        current_directory = item
        config.add_recent_folder(str(item))
        return f"Opened folder {item.name}"

    return f"Opened file {item.name}"


def _search_current_directory(target: str):

    target = target.lower().strip()

    # 1. Exact filename (with extension)
    for item in current_directory.iterdir():

        if item.name.lower() == target:

            return _open_item(item)

    # 2. Exact filename (without extension)
    for item in current_directory.iterdir():

        if item.stem.lower() == target:

            return _open_item(item)

    # 3. Partial match
    for item in current_directory.iterdir():

        if target in item.stem.lower():

            return _open_item(item)

    return "File or Folder not found."


def execute(intent):

    global current_directory

    if not intent:
        return "Unknown command."

    intent_name = intent.get("intent")

    try:
        if intent_name == "pwd":
            return f"Current Directory:\n{current_directory}"

        if intent_name == "list_files":
            return _format_directory_listing(os.listdir(current_directory))

        if intent_name == "create_folder":
            folder = current_directory / intent.get("target", "").strip()

            if not folder.name:
                return "Folder name is required."

            folder.mkdir(exist_ok=True)
            config.add_recent_folder(str(folder))
            logger.info("Created folder: %s", folder)
            return f"Folder '{intent.get('target', '')}' created."

        if intent_name == "open":
            return _search_current_directory(intent.get("target", ""))

        if intent_name == "open_app":
            launch_result = launcher.launch(intent.get("target", ""))
            return launch_result.message

        if intent_name == "search":
            query = intent.get("target", "")
            matches = search_index.search(query)

            if not matches:
                return f"No matches found for '{query}'."

            lines = [f"{index + 1}. {item.name} - {item.path}" for index, item in enumerate(matches)]
            return "\n".join(lines)

        if intent_name == "exit":
            return "Goodbye!"

        return "Unknown command."

    except Exception as exc:
        logger.exception("Command execution failed: %s", intent)
        return f"Error: {exc}"