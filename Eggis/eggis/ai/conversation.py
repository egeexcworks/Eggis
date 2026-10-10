"""Groq-backed conversation for Eggis.

Reads GROQ_API_KEY from .env (via python-dotenv). Keeps a short rolling
history so follow-up questions like "and why?" have context.

Fails loudly and specifically -- never fabricates an answer.
"""

from __future__ import annotations

import os
from typing import List, Dict

from dotenv import load_dotenv

try:
    from groq import Groq
except ImportError:  # pragma: no cover
    Groq = None  # type: ignore[assignment]


DEFAULT_MODEL = "openai/gpt-oss-120b"
MAX_HISTORY_MESSAGES = 12  # user+assistant pairs, trimmed from the front

SYSTEM_PROMPT = (
    "You are Eggis, the personal assistant inside a Python project on "
    "the user's Windows desktop. Your developer is the user, who goes by "
    "egeexc. You are NOT ChatGPT, you are NOT made by OpenAI, you are "
    "the assistant component of the Eggis project, running on a language "
    "model through the Groq API. You have exactly the tools the user's "
    "project exposes (help, time, about, calc, solve, reset, exit). If "
    "you are asked to do something those tools cannot do (open apps, "
    "browse the web, send emails), say clearly that you can't do that "
    "yet -- do NOT pretend to do it. Answer concisely. If unsure, say so."
)


class ConversationError(RuntimeError):
    """Raised when the AI backend cannot produce a reply."""


class Conversation:
    """Stateful conversation wrapper around the Groq chat API."""

    def __init__(self, model: str = DEFAULT_MODEL) -> None:
        load_dotenv()
        api_key = os.environ.get("GROQ_API_KEY", "").strip()

        if not api_key:
            raise ConversationError(
                "GROQ_API_KEY is not set. Create a .env file in the project "
                "root with the line: GROQ_API_KEY=your_key_here"
            )
        if Groq is None:
            raise ConversationError(
                "The 'groq' package is not installed. Run: "
                "python -m pip install groq"
            )

        self._model = model
        self._client = Groq(api_key=api_key)
        self._history: List[Dict[str, str]] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    def _trim_history(self) -> None:
        # Keep system prompt + the last MAX_HISTORY_MESSAGES non-system messages.
        system = self._history[0]
        rest = self._history[1:]
        if len(rest) > MAX_HISTORY_MESSAGES:
            rest = rest[-MAX_HISTORY_MESSAGES:]
        self._history = [system] + rest

    def reply(self, user_text: str) -> str:
        """Send user_text to the model and return the assistant's reply."""
        if not user_text or not user_text.strip():
            return ""

        self._history.append({"role": "user", "content": user_text.strip()})
        self._trim_history()

        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=self._history,
                temperature=0.6,
                max_tokens=1024,
                timeout=30.0,
            )
        except Exception as exc:  # noqa: BLE001
            # Roll back the user message so history stays consistent
            self._history.pop()
            raise ConversationError(f"AI request failed: {exc}") from exc

        if not response.choices:
            self._history.pop()
            raise ConversationError("AI returned no choices.")

        message = response.choices[0].message
        content = (message.content or "").strip() if message else ""

        if not content:
            self._history.pop()
            raise ConversationError("AI returned an empty response.")

        self._history.append({"role": "assistant", "content": content})
        self._trim_history()
        return content

    def reset(self) -> None:
        """Clear conversation history, keeping the system prompt."""
        self._history = [{"role": "system", "content": SYSTEM_PROMPT}]


if __name__ == "__main__":
    # Manual smoke test:  python -m eggis.ai.conversation "your question"
    import sys

    question = " ".join(sys.argv[1:]) or "Say hello in one short sentence."
    conv = Conversation()
    print(conv.reply(question))
