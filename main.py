import speech
import commands
import file_manager

while True:

    command = speech.listen()

    if command == "":
        continue

    if command == "exit":
        break

    intent = commands.detect_intent(command)
    print(intent)
    result = file_manager.execute(intent)

    print(result)