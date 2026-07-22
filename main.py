import core.speech as speech
from core.assistant import handle_command
from core.logger import configure_logging

configure_logging()

while True:

    command = speech.listen()
    command, result = handle_command(command)

    if command == "":
        continue

    print(result)

    if command == "exit":
        break