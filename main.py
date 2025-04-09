from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from app.instruments.main_view import MainView
from app.gcs import GCS
from communication.radio import Radio


# 2. Get it working with preflight sidebar removed
# 3. Test qpainter writing to QWidget instead of canvas
# 4. rename everything

if __name__ == "__main__":
    # if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    #     QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    # if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    #     QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication([])

    gcs = GCS()
    radio = Radio()

    main_window = MainView(app, radio, gcs)
    # main_window.showFullScreen()
    main_window.showMaximized()
    
    app.exec()