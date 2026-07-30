from engines.game import GameEngine

if __name__ == "__main__":
    try:
        GameEngine().handle()

    except KeyboardInterrupt:
        print("\nExiting...")
