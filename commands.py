def detect_intent(command):

    words = command.split()
    print(words)
    if not words:
        return None

    action = words[0]

    if action == "open":
        return {
            "intent": "open",
            "target": " ".join(words[1:])
        }

    elif action == "create":
        if len(words) >= 3 and words[1] == "folder":
            return {
                "intent": "create_folder",
                "target": " ".join(words[2:])
            }

    elif action == "list":
        if len(words) >= 2 and words[1] == "files":
            return {
                "intent": "list_files"
            }

    elif action == "current":
        if len(words) >= 2 and words[1] == "directory":
            return {
                "intent": "pwd"
            }

    return {
        "intent": "unknown"
    }