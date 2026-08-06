from engines.game import GameEngine

if __name__ == "__main__":
    try:
        GameEngine().handle_menu()

    except KeyboardInterrupt:
        print("\n\tExiting...")
