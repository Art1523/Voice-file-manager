import speech
import commands
import file_manager
import speaker

while True:

    command = speech.listen()

    if command == "":
        continue

    if command == "exit":
        speaker.speak("Goodbye!")
        break

    intent = commands.detect_intent(command)

    result = file_manager.execute(intent)

    print(result)

    speaker.speak(result)