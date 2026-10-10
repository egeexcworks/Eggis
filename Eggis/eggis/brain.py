
from eggis.tools.system import handle_system_command


HELP_TEXT = """
Available commands:
  help   - Show available commands
  time   - Display the current local time
  about  - Show information about Eggis
  exit   - Close Eggis
"""


def process_command(user_input: str) -> str:
    """Interpret a text command and return Eggis's response."""

    command = user_input.strip().lower()

    if not command:
        return ""

    if command == "help":
        return HELP_TEXT.strip()

    response = handle_system_command(command)

    if response is not None:
        return response

    return (
        f"I don't understand '{user_input.strip()}' yet.\n"
        "Type 'help' to see the commands I understand."
    )
