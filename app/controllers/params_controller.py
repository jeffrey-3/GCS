from PyQt5.QtWidgets import *
import json

class ParamsController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.view.params_btn.clicked.connect(self.open_params)

        # Load default
        self.model.process_params_file("app/resources/last_params.json")
        display_text = ""
        for param in self.model.get_params_json():
            display_text += param["name"] + "\t"
            display_text += str(param["value"]) + "\n"
        self.view.file_view.setPlainText(display_text)

    def open_params(self):
        file_path, _ = QFileDialog.getOpenFileName(self.view, "Open File", "", "All Files (*)")
        if file_path:
            if self.model.process_params_file(file_path):
                self.view.params_file_input.setPlainText(file_path)

                display_text = ""
                for param in self.model.get_params_json():
                    display_text += param["name"] + "\t"
                    display_text += param["value"] + "\n"
                self.view.file_view.setPlainText(display_text)
            else:
                QMessageBox.information(self.view, "Error", "File format incorrect")