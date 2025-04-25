from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import json
from gcs import *

class ParamsView(QWidget):
    def __init__(self, gcs: GCS):
        super().__init__()
        self.gcs = gcs

        self.params = []

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QLabel("<h1>Parameters</h1>"))

        self.file_path_label = QLabel("File Directory: Default")
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
                self.gcs.upload_params(self.params)
            else:
                QMessageBox.information(self, "Error", "File format incorrect")
    
    def process_params_file(self, path):
        try:
            file = open(path, "r")
            params_json = json.load(file)
            self.params = [Parameter(param["name"], param["value"], param["type"]) for param in params_json]
            return True
        except Exception as e:
            print(f"Error processing params file: {e}")
            return False
    
    def upload_to_vehicle(self):
        if len(self.params) > 0:
            self.gcs.send_params(self.params)
            self.save_params(self.params)
            QMessageBox.about(self, "Status", "Successfully uploaded parameters")
        else:
            QMessageBox.information(self, "Error", "No parameters set")
    
    def save_params(self, params):
        json_data = [
            {"name": param.name, "value": param.value, "type": param.type} 
            for param in params
        ]

        f = open("resources/last_params.json", 'w')
        json.dump(json_data, f, indent=4)

        print("Last params saved")