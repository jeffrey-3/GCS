from PyQt5.QtWidgets import QApplication
from app.views.main_view import MainView
from app.controllers.main_controller import MainController
from app.models.telemetry_model import TelemetryModel
from app.models.config_model import ConfigModel

if __name__ == "__main__":
    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication([])

    config_model = ConfigModel()
    telemetry_model = TelemetryModel()

    main_window = MainView(app, telemetry_model, config_model)
    main_controller = MainController(main_window, telemetry_model, config_model)
    main_window.showFullScreen()
    
    app.exec() 