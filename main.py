from PyQt5.QtWidgets import QApplication
from app.main_window import MainWindow

if __name__ == "__main__":
    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication([])
    main_window = MainWindow(app)
    main_window.showMaximized()
    app.exec()