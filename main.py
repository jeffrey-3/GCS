from PyQt5.QtWidgets import QApplication
from controller import Controller
from view import StartupView, MainView
from model import Model

if __name__ == "__main__":
    app = QApplication([])

    model = Model()
    main_view = MainView()
    startup_view = StartupView(app)
    controller = Controller(model, startup_view, main_view)
    
    startup_view.set_controller(controller)
    startup_view.show()

    app.exec()