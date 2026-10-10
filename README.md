
# Eggis

Eggis is a personal AI assistant for Windows, written in Python. It runs as
a text REPL with spoken replies, routes simple commands locally, and falls
back to a cloud language model for open-ended questions.

This is an early-stage project. The architecture is deliberately small and
each piece is replaceable.

## Features

- **Spoken replies.** Every response is spoken aloud via the Windows SAPI
  text-to-speech engine (`pyttsx3`).
- **Command router.** Local commands are handled without any network call,
  so they are instant and reliable.
- **Math tools.** `calc` evaluates arithmetic expressions; `solve` solves
  equations. Powered by `sympy` with a restricted parser (no `eval()`).
- **App / URL launcher.** `open <target>` opens a URL, a known site name,
  or a file path with the Windows default handler.
- **AI conversation.** Anything that is not a local command is sent to a
  Groq-hosted model (`openai/gpt-oss-120b` by default). The assistant keeps
  a short conversation history so follow-up questions work.

## Not yet implemented

- Microphone input / speech recognition.
- Wake word.
- Persistent memory across sessions (`eggis/memory.py` is a placeholder).

These are planned but not present. The README will be updated when they land.

## Requirements

- Windows 10 or 11.
- Python 3.12 (3.13/3.14 are not yet tested against `pyttsx3` on this setup).
- A free Groq API key: https://console.groq.com/keys

## Installation

From the project root:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
