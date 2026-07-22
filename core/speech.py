import speech_recognition as sr
from core.app_config import AppConfig
from core.logger import get_logger

recognizer = sr.Recognizer()
config = AppConfig()
logger = get_logger(__name__)

def listen():
    config.reload()
    microphone_index = config.get("microphone", 0)

    try:
        with sr.Microphone(device_index=microphone_index) as source:
            print("Listening...")

            recognizer.adjust_for_ambient_noise(source, duration=1)

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=5,
            )

        try:
            command = recognizer.recognize_google(audio)

            print("You said:", command)

            return command.lower()

        except sr.UnknownValueError:
            logger.warning("Speech was not understood.")
            print("Sorry, I couldn't understand.")

            return ""
        except sr.WaitTimeoutError:
            logger.warning("Speech input timed out.")
            print("Listening timed out.")

            return ""
    except sr.RequestError:
        logger.error("Speech recognition request failed.")
        print("Internet problem.")

        return ""
    except OSError as exc:
        logger.exception("Microphone error")
        print(f"Microphone error: {exc}")

        return ""
    