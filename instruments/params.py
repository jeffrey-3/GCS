from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import json

class ParamsView(QWidget):
    def __init__(self, gcs):
        super().__init__()
        self.gcs = gcs

        self.params_json = None

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QLabel("<h1>Parameters</h1>"))

        self.file_path_label = QLabel("File Directory:")
        self.file_path_label.setStyleSheet("font-size: 12pt;")
        self.layout.addWidget(self.file_path_label)

        self.params_btn = QPushButton("Import File")
        self.params_btn.setStyleSheet("font-size: 12pt;")
        self.params_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.layout.addWidget(self.params_btn)

        self.upload_btn = QPushButton("Upload to Vehicle")
        self.upload_btn.setStyleSheet("font-size: 12pt;")
        self.upload_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.layout.addWidget(self.upload_btn)

        self.layout.addStretch()

        self.params_btn.clicked.connect(self.open_params)
        self.upload_btn.clicked.connect(self.upload_to_vehicle)
        self.process_params_file("resources/last_params.json")
    
    def open_params(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        if file_path:
            if self.process_params_file(file_path):
                self.file_path_label.setText("File Directory: " + file_path)
            else:
                QMessageBox.information(self, "Error", "File format incorrect")
    
    def process_params_file(self, path):
        try:
            file = open(path, "r")
            self.params_json = json.load(file)
            print(self.params_json)
            return True
        except Exception as e:
            print(f"Error processing params file: {e}")
            return False
    
    def upload_to_vehicle(self):
        if self.params_json:
            return
        else:
            QMessageBox.information(self, "Error", "No parameters set")