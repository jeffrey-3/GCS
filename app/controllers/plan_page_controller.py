from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class PlanPageController(QObject):
    complete_signal = pyqtSignal()
    center_map_signal = pyqtSignal()

    def __init__(self, view, model):
        super().__init__()
        self.view = view
        self.model = model
        self.view.next_btn.clicked.connect(self.next)
        self.view.center_btn.clicked.connect(self.center_map)
    
    def next(self):
        if self.model.get_waypoints():
            self.complete_signal.emit()
        else:
            QMessageBox.information(self.view, "Error", "Flight plan missing")
    
    def center_map(self):
        self.center_map_signal.emit()