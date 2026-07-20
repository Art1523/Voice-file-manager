from pathlib import Path
import os

current_directory = Path.home()
print("Home Path:", Path.home())
print("Current Directory:", current_directory)

def execute(intent):

    global current_directory

    if intent["intent"] == "pwd":

        return f"Current Directory:\n{current_directory}"

    elif intent["intent"] == "list_files":

        files = os.listdir(current_directory)

        if not files:
            return "Folder is empty."

        return "\n".join(files)

    elif intent["intent"] == "create_folder":

        folder = current_directory / intent["target"]

        folder.mkdir(exist_ok=True)

        return f"Folder '{intent['target']}' created."

    elif intent["intent"] == "open":

        folder = current_directory / intent["target"]

        if folder.exists():

            current_directory = folder

            return f"Opened {folder}"

        return "Folder not found."

    return "Unknown command."