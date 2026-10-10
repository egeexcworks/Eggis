from eggis.tools.system import handle_system_command
from eggis.tools.math_tools import handle_math_command
from eggis.ai.conversation import Conversation, ConversationError


HELP_TEXT = """
Available commands:
  help              - Show available commands
  time              - Display the current local time
  about             - Show information about Eggis
  calc <expr>       - Evaluate a math expression (e.g. calc 2+2*5)
  solve <equation>  - Solve an equation (e.g. solve 2*x+3=11)
  reset             - Clear the AI's conversation memory
  exit              - Close Eggis

Anything else is sent to the AI and answered conversationally.
"""


_conversation = None


def _get_conversation() -> Conversation:
    global _conversation
    if _conversation is None:
        _conversation = Conversation()
    return _conversation


def process_command(user_input: str) -> str:
    """Interpret a text command and return Eggis's response."""

    command = user_input.strip().lower()

    if not command:
        return ""

    if command == "help":
        return HELP_TEXT.strip()

    if command == "reset":
        _get_conversation().reset()
        return "Conversation memory cleared."

    response = handle_system_command(command)
    if response is not None:
        return response

    response = handle_math_command(command)
    if response is not None:
        return response

    try:
        return _get_conversation().reply(user_input)
    except ConversationError as exc:
        return f"I couldn't reach my AI backend: {exc}"
