from PyQt5.QtWidgets import QApplication
from controller import Controller
from view import View
from model import Model

if __name__ == "__main__":
    app = QApplication([])

    model = Model()
    view = View(app)
    controller = Controller(model, view)

    view.show()
    app.exec()