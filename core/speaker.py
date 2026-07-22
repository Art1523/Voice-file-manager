from pathlib import Path
import threading
import pyttsx3
from core.app_config import AppConfig
from core.logger import get_logger

logger = get_logger(__name__)

engine = pyttsx3.init()
config = AppConfig()
engine.setProperty("rate", config.get("speech_speed", 170))

voices = engine.getProperty("voices")
if voices:
    engine.setProperty("voice", voices[0].id)


def speak(text):
    """Speak assistant output without blocking the UI thread."""

    try:
        config.reload()
        engine.setProperty("rate", config.get("speech_speed", 170))

        voices = engine.getProperty("voices")
        if voices:
            engine.setProperty("voice", voices[0].id)

        if "Current Directory:" in text:
            path = text.replace("Current Directory:", "").strip()
            folder_name = Path(path).name or "home"
            speech_text = f"You are currently in the {folder_name} folder."
        else:
            speech_text = text

        logger.info("Assistant spoke: %s", speech_text)
        print("Assistant:", speech_text)

        thread = threading.Thread(target=_speak_sync, args=(speech_text,), daemon=True)
        thread.start()
    except Exception as exc:
        logger.exception("TTS failed: %s", exc)


def _speak_sync(text: str) -> None:
    try:
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as exc:
        logger.exception("Background TTS failed: %s", exc)