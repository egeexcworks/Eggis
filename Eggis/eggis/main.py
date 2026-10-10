
from eggis.brain import process_command


def main() -> None:
    print("=" * 40)
    print("             EGGIS v0.1.0")
    print("       Your personal assistant")
    print("=" * 40)
    print("Eggis is online. Type 'help' to begin.")
    print("")

    while True:
        try:
            user_input = input("You > ").strip()

            if user_input.lower() == "exit":
                print("Eggis > Shutting down. See you later!")
                break

            response = process_command(user_input)

            if response:
                print(f"\nEggis > {response}\n")

        except (KeyboardInterrupt, EOFError):
            print("\nEggis > Shutting down safely.")
            break


if __name__ == "__main__":
    main()
