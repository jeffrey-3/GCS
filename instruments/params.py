from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class ParamsView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QLabel("<h1>Parameters</h1>"))

        self.layout.addWidget(QLabel("<div style='font-size: 12pt;'>File Directory:</div>"))

        self.params_btn = QPushButton("Import File")
        self.params_btn.setStyleSheet("font-size: 12pt;")
        self.params_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.layout.addWidget(self.params_btn)

        self.upload_btn = QPushButton("Upload to Vehicle")
        self.upload_btn.setStyleSheet("font-size: 12pt;")
        self.upload_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.layout.addWidget(self.upload_btn)

        self.layout.addStretch()