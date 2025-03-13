from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class ReconnectPageController(QObject):
    complete_signal = pyqtSignal()

    def __init__(self, view, model):
        super().__init__()
        self.view = view
        self.model = model
        self.view.next_btn.clicked.connect(self.next)
    
    def next(self):
        if self.model.connect():
            self.complete_signal.emit()
        else:
            QMessageBox.information(self.view, "Error", "COM port incorrect")