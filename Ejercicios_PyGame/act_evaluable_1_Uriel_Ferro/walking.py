import sys
from walking_girl_app import Game

def main():
    print("Iniciador del juego ejecutándose.")
    app = Game()
    app.run()

if __name__ == "__main__":
    sys.exit(main()) 