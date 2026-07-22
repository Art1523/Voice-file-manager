# VoiceFileManager / ART AI

A voice-first desktop assistant for file management and application launching.

## Current Capabilities

- Speech recognition input
- Offline text-to-speech output
- Shared voice and text command pipeline
- Intent detection for file commands
- Open files and folders
- Create folders
- List files
- Current directory reporting
- Application launcher support
- Global file search across common Windows folders
- JSON-backed settings storage
- JSON-backed command history
- Rotating log file output
- Thread-safe CustomTkinter UI with chat bubbles and animated orb

## Architecture

- `core/` contains assistant orchestration, command parsing, file operations, history, logging, search, and app launching
- `ui/` contains the CustomTkinter desktop experience
- `assets/` stores configuration and cached data
- `tests/` contains unit tests for command and history behavior

## Status

ART AI refactor in progress. Core assistant flow is now centralized and the GUI uses background threads safely.