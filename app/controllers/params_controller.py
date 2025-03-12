from PyQt5.QtWidgets import *

class ParamsController:
    def __init__(self, view, model):
        self.view = view
        self.model = model

        self.view.params_btn.clicked.connect(self.open_params)

    def open_params(self):
        file_path, _ = QFileDialog.getOpenFileName(self.view, "Open File", "", "All Files (*)")
        if file_path:
            if self.model.process_params_file(file_path):
                self.view.params_file_input.setPlainText(file_path)
            else:
                QMessageBox.information(self.view, "Error", "File format incorrect")