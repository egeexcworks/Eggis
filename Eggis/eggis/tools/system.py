
from datetime import datetime


def handle_system_command(command: str) -> str | None:
    """Handle Eggis's built-in system commands."""

    if command == "time":
        current_time = datetime.now().astimezone()
        return f"The current time is {current_time.strftime('%I:%M:%S %p')}."

    if command == "about":
        return (
            "I am Eggis, your personal AI assistant.\n"
            "Version: 0.1.0\n"
            "Status: Early development"
        )

    return None
