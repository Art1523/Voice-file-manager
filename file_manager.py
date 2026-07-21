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

        target = intent["target"].lower().strip()

        # 1. Exact filename (with extension)
        for item in current_directory.iterdir():

            if item.name.lower() == target:

                os.startfile(item)

                if item.is_dir():
                    current_directory = item
                    return f"Opened folder {item.name}"

                return f"Opened file {item.name}"

        # 2. Exact filename (without extension)
        for item in current_directory.iterdir():

            if item.stem.lower() == target:

                os.startfile(item)

                if item.is_dir():
                    current_directory = item
                    return f"Opened folder {item.name}"

                return f"Opened file {item.name}"

        # 3. Partial match
        for item in current_directory.iterdir():

            if target in item.stem.lower():

                os.startfile(item)

                if item.is_dir():
                    current_directory = item
                    return f"Opened folder {item.name}"

                return f"Opened file {item.name}"

        return "File or Folder not found."

    return "Unknown command."