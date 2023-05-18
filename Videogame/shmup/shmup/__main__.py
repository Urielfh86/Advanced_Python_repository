import sys
from shmup.shmup import Game

def main(args = None):
    if args is None:
        args = sys.argv[1:]

    print("Main module speaking")
    app = Game()
    app.run()

if __name__ == '__main__': # Esto se ejecutará cuando el paquete shump sea llamado desde consola como un ejecutable "python -m shmup"
    sys.exit(main())       # En realidad no queremos que sea llamado de esta manera, pero nos cubrimos por las dudas para que si pasa el programa 
                           # siga funcionando igual.

