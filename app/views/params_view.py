from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class ParamsView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel("<h1>Parameters</h1>"))

        self.params_file_input = QPlainTextEdit()
        self.params_btn = QPushButton("Import Parameters")
        
        self.params_file_input.setStyleSheet("font-size: 12pt;")
        self.params_btn.setStyleSheet("font-size: 12pt;")

        self.layout.addWidget(self.params_file_input)
        self.layout.addWidget(self.params_btn)

        self.setLayout(self.layout)