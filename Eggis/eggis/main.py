
from eggis.brain import process_command
from eggis.voice.text_to_speech import EggisSpeaker


EGGIS_VOICE_ID = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0"


def main() -> None:
    speaker = EggisSpeaker(voice_id=EGGIS_VOICE_ID)

    print("=" * 40)
    print("             EGGIS v0.1.0")
    print("       Your personal assistant")
    print("=" * 40)
    print("Eggis is online. Type 'help' to begin.")
    print("")

    greeting = "Eggis is online. How can I help you?"
    speaker.speak(greeting)

    while True:
        try:
            user_input = input("You > ").strip()

            if user_input.lower() == "exit":
                farewell = "Shutting down. See you later!"
                print(f"Eggis > {farewell}")
                speaker.speak(farewell)
                break

            response = process_command(user_input)

            if response:
                print(f"\nEggis > {response}\n")
                speaker.speak(response)

        except (KeyboardInterrupt, EOFError):
            farewell = "Shutting down safely."
            print(f"\nEggis > {farewell}")
            speaker.speak(farewell)
            break


if __name__ == "__main__":
    main()
