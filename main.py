from PyQt5.QtWidgets import QApplication
from app.main_window import MainWindow

if __name__ == "__main__":
    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication([])
    main_window = MainWindow(app)
    main_window.showFullScreen()
    app.exec()


# Does not deselect when testing started and you have selected

# Deleting last waypoint doesn't work