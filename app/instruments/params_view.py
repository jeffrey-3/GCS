from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class ParamsView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QLabel("<h1>Parameters</h1>"))

        self.file_view = QPlainTextEdit()
        self.file_view.setStyleSheet("font-size: 12pt;")
        self.file_view.setReadOnly(True)
        self.layout.addWidget(self.file_view)

        self.layout.addWidget(QLabel("<div style='font-size: 12pt;'>File Directory:</div>"))

        self.params_file_input = QPlainTextEdit()
        self.params_file_input.setFixedHeight(200)
        self.params_file_input.setStyleSheet("font-size: 12pt;")
        self.params_file_input.setReadOnly(True)
        self.layout.addWidget(self.params_file_input)

        self.params_btn = QPushButton("Import Parameters")
        self.params_btn.setStyleSheet("font-size: 12pt;")
        self.layout.addWidget(self.params_btn)