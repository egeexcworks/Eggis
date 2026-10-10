"""Text-to-speech for Eggis.

Wraps pyttsx3 behind a small, replaceable interface. If the
speech engine fails, speak() returns False and the caller can
decide what to do -- it never pretends text was spoken.
"""

from __future__ import annotations

from typing import Optional

try:
    import pyttsx3
except ImportError:  # pragma: no cover - handled at runtime
    pyttsx3 = None  # type: ignore[assignment]


class EggisSpeaker:
    """Speak text aloud using the system text-to-speech engine.

    The engine is created lazily on first use, because creating it
    at import time can fail on machines with no audio device and
    would break `import eggis.voice.text_to_speech`.
    """

    def __init__(
        self,
        rate: Optional[int] = None,
        volume: Optional[float] = None,
        voice_id: Optional[str] = None,
    ) -> None:
        self._engine = None
        self._rate = rate
        self._volume = volume
        self._voice_id = voice_id

    def _ensure_engine(self):
        if self._engine is not None:
            return self._engine

        if pyttsx3 is None:
            raise RuntimeError(
                "pyttsx3 is not installed. Run: python -m pip install pyttsx3"
            )

        engine = pyttsx3.init()

        if self._rate is not None:
            engine.setProperty("rate", self._rate)
        if self._volume is not None:
            engine.setProperty("volume", self._volume)
        if self._voice_id is not None:
            engine.setProperty("voice", self._voice_id)

        self._engine = engine
        return engine

    def speak(self, text: str) -> bool:
        """Speak `text` aloud. Returns True on success, False on failure.

        Empty or whitespace-only text is treated as success and does
        nothing -- callers can safely pass any string.
        """
        if text is None:
            return True
        stripped = text.strip()
        if not stripped:
            return True

        try:
            engine = self._ensure_engine()
            engine.say(stripped)
            engine.runAndWait()
            return True
        except Exception as exc:  # noqa: BLE001 - report, don't crash the app
            print(f"[EggisSpeaker] speech failed: {exc}")
            return False

    def list_voices(self):
        """Return available voices. Useful for picking a voice_id."""
        engine = self._ensure_engine()
        return engine.getProperty("voices")

    def stop(self) -> None:
        """Stop any current speech and release the engine."""
        if self._engine is None:
            return
        try:
            self._engine.stop()
        except Exception:
            pass
        self._engine = None


if __name__ == "__main__":
    # Quick manual check:  python -m eggis.voice.text_to_speech
    speaker = EggisSpeaker()
    ok = speaker.speak("Hello. I am Eggis. My voice module is working.")
    print("speak() returned:", ok)
