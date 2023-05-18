import sys
from marquee_app import Game

def main():
    print("Main talking")
    app = Game()
    app.run()

if __name__ == "__main__":
    sys.exit(main())