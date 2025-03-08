from PyQt5.QtWidgets import QApplication
from app.controllers.controller import Controller
from app.main_window import View
from app.models.model import Model

if __name__ == "__main__":
    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication([])

    model = Model()
    view = View(app)
    controller = Controller(model, view)

    view.showMaximized()

    app.exec()