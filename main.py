from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from app.views.main_view import MainView
from app.controllers.main_controller import MainController
from app.models.config_model import ConfigModel
from communication.radio import Radio

if __name__ == "__main__":
    # if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    #     QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    # if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    #     QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication([])

    config_model = ConfigModel()
    radio = Radio()

    main_window = MainView(app, radio, config_model)
    main_controller = MainController(main_window, radio, config_model)
    # main_window.showFullScreen()
    main_window.show()
    
    app.exec()