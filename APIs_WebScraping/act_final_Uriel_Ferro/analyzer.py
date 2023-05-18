# Aplicación que brinda información de acciones de la bolsa de Estados Unidos utilizando la API de Alpha Vantage.

import sys
from PyQt6.QtWidgets import QApplication
from view import View
from model import Model
from controller import Controller

def main():
    analyzer = QApplication(sys.argv)

    view = View()
    view.show()

    model = Model()
    controller = Controller(view, model)

    sys.exit(analyzer.exec())

if __name__ == '__main__':
    main()