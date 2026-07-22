# ART AI

> A voice-first desktop assistant built in Python for file management, app launching, and hands-free interaction.

![ART AI Preview](https://img.shields.io/badge/Status-Active%20Development-brightgreen)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![UI](https://img.shields.io/badge/UI-CustomTkinter-4ea8de)
![Voice](https://img.shields.io/badge/Voice-Speech%20Recognition-ff6b6b)

## ✨ What This Project Is

ART AI is a personal desktop assistant designed to make everyday computer tasks feel more natural. Instead of clicking through folders or typing long commands, users can interact through voice or text.

The project blends:
- voice interaction
- file and folder operations
- app launching
- search across common locations
- a modern desktop experience

It is built as both a practical tool and a polished Python project to explore AI-style interaction in a desktop environment.

## 🚀 Core Features

- Voice command input with speech recognition
- Offline text-to-speech responses
- Text-based command support
- File and folder operations
- Current directory awareness
- Search across common Windows folders
- Application launching support
- Persistent history and settings
- Thread-safe desktop UI with chat-style interaction

## 🛠 Tech Stack

- Python
- CustomTkinter for the desktop interface
- SpeechRecognition for voice input
- pyttsx3 for offline text-to-speech
- JSON-based configuration and history storage
- Modular Python architecture for extensibility

## 🧠 How It Works

1. The user enters a voice or text command.
2. The assistant identifies the intent.
3. The relevant tool or file operation is executed.
4. The result is shown in the UI and spoken back when appropriate.

## ▶️ Getting Started

### Install dependencies

```bash
pip install customtkinter speechrecognition pyttsx3
```

### Run the app

```bash
python -m ui.app
```

> If you are using a microphone, make sure your system audio input is available.

## 📁 Project Structure

```text
core/         # assistant logic, command handling, search, file operations, speaker, speech
ui/           # CustomTkinter desktop interface
assets/      # config, conversation memory, and history data
tests/       # unit tests for core behavior
```

## 🧩 Architecture Highlights

- Centralized assistant orchestration
- Separate modules for speech, TTS, file handling, search, and UI
- Background worker threads for responsive interaction
- Configurable settings and history persistence

## 🔮 Future Direction

Planned improvements include:
- smarter command understanding
- better memory and context handling
- richer local AI integrations
- more polished desktop workflows

## 📌 Status

ART AI is currently in active development, with a working desktop experience and a modular backend that continues to evolve.

## 🤝 Contributing

Contributions, ideas, and improvements are welcome. If you would like to improve the assistant experience, feel free to open an issue or submit a pull request.
