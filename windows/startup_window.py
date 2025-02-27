from PyQt5.QtWidgets import QMainWindow, QGridLayout, QLabel, QSizePolicy, QLineEdit, QPushButton, QWidget, QFileDialog
from PyQt5.QtCore import Qt
from windows.main_window import MainWindow

class ConfigWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.flight_plan_dir = ""
        self.params_dir = ""

        self.initUI()
        self.show()

    def initUI(self):
        self.setWindowTitle("UAV Ground Control")
        
        self.layout = QGridLayout()

        self.title_label = QLabel("<h1>UAV Ground Control<\h1>")
        self.layout.addWidget(self.title_label, 0, 0, 1, 2)

        self.flight_plan_label = QLabel("Flight Plan:")
        self.layout.addWidget(self.flight_plan_label, 1, 0)

        self.parameters_label = QLabel("Parameters:")
        self.layout.addWidget(self.parameters_label, 2, 0)

        # Set previous directories as default
        f = open("resources/last_dir.txt", "r")
        self.label1 = QLineEdit(f.readline())
        self.label2 = QLineEdit(f.readline())
        self.layout.addWidget(self.label1, 1, 1)
        self.layout.addWidget(self.label2, 2, 1)

        self.label1.setFixedWidth(1000)
        self.label2.setFixedWidth(1000)

        self.label1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.label2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.load_button1 = QPushButton("Search")
        self.load_button1.clicked.connect(self.load_file1)
        self.layout.addWidget(self.load_button1, 1, 2)

        self.load_button2 = QPushButton("Search")
        self.load_button2.clicked.connect(self.load_file2)
        self.layout.addWidget(self.load_button2, 2, 2)

        self.continue_button = QPushButton("OK")
        self.continue_button.clicked.connect(self.continue_process)
        self.layout.addWidget(self.continue_button, 3, 0, 1, 3)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def load_file1(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load File 1", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            self.label1.setText(file_name)

    def load_file2(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load File 2", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            self.label2.setText(file_name)

    def continue_process(self):
        # Strip to remove newline character
        self.flight_plan_dir = self.label1.text().strip()
        self.params_dir = self.label2.text().strip()

        if self.flight_plan_dir and self.params_dir:
            # Save to memory
            f = open("resources/last_dir.txt", "w")
            f.write(self.flight_plan_dir + "\n")
            f.write(self.params_dir)

            self.main = MainWindow(self.flight_plan_dir, self.params_dir)
            self.close()
