from pathlib import Path
import pyttsx3

def speak(text):

    engine = pyttsx3.init()

    engine.setProperty("rate", 170)

    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)

    # ---------- Make speech more natural ----------

    if "Current Directory:" in text:

        path = text.replace("Current Directory:", "").strip()

        folder_name = Path(path).name

        if folder_name == "":
            folder_name = "home"

        speech_text = f"You are currently in the {folder_name} folder."

    else:

        speech_text = text

    print("Assistant:", speech_text)

    engine.say(speech_text)

    engine.runAndWait()

    engine.stop()