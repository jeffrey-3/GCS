import pyqtgraph as pg
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)

        for i in range(3):
            self.add()

    def add(self):
        plot_graph = pg.PlotWidget()
        time = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 30]
        plot_graph.plot(time, temperature)
        self.main_layout.addWidget(plot_graph)

app = QApplication([])
main = MainWindow()
main.show()
app.exec()