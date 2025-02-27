from PyQt5.QtWidgets import QMainWindow, QGridLayout, QLabel, QSizePolicy, QLineEdit, QPushButton, QWidget, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from widgets.main_window import MainWindow

class View(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.flight_plan_dir = ""
        self.params_dir = ""
        self.init_ui()
        self.apply_dark_theme()
    
    def init_ui(self):
        """Initialize the UI components"""
        self.setWindowTitle("UAV Ground Control")
        self.setup_layout()
        self.setup_connections()

    def setup_layout(self):
        """Set up the layout and widgets"""
        self.layout = QGridLayout()

        # Get default directories
        default_dirs_file = open("resources/last_dir.txt", "r")
        default_flightplan_dir = default_dirs_file.readline()
        default_params_dir = default_dirs_file.readline()

        # Title
        self.title_label = QLabel("<h1>UAV Ground Control<\h1>")
        self.layout.addWidget(self.title_label, 0, 0, 1, 2)

        # Flight Plan Section
        self.flight_plan_label = QLabel("Flight Plan:")
        self.flightplan_input = QLineEdit(default_flightplan_dir)
        self.flightplan_input.setFixedWidth(1000)
        self.flightplan_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.flightplan_btn = QPushButton("Search")
        self.layout.addWidget(self.flight_plan_label, 1, 0)
        self.layout.addWidget(self.flightplan_input, 1, 1)
        self.layout.addWidget(self.flightplan_btn, 1, 2)

        # Parameters section
        self.parameters_label = QLabel("Parameters:")
        self.params_input = QLineEdit(default_params_dir)
        self.params_input.setFixedWidth(1000)
        self.params_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.params_btn = QPushButton("Search")
        self.layout.addWidget(self.parameters_label, 2, 0)
        self.layout.addWidget(self.params_input, 2, 1)
        self.layout.addWidget(self.params_btn, 2, 2)

        # Continue button
        self.continue_button = QPushButton("OK")
        self.layout.addWidget(self.continue_button, 3, 0, 1, 3)

        # Set layout
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)
    
    def setup_connections(self):
        """Connect signals to slots"""
        self.flightplan_btn.clicked.connect(lambda: self.load_file(self.flightplan_input))
        self.params_btn.clicked.connect(lambda: self.load_file(self.params_input))
        self.continue_button.clicked.connect(self.continue_process)

    def load_file(self, target_input):
        """Open a file dialog and set the selected file path to the target input"""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Load File", "", "All Files (*);;Text Files (*.txt)", options=options
        )
        if file_name:
            target_input.setText(file_name)

    def continue_process(self):
        """Handle the OK button click"""
        self.flight_plan_dir = self.flightplan_input.text().strip()
        self.params_dir = self.params_input.text().strip()

        if self.flight_plan_dir and self.params_dir:
            self.save_last_directories()
            self.open_main_window()
    
    def save_last_directories(self):
        """Save the last used directories to a file"""
        f = open("resources/last_dir.txt", "w")
        f.write(f"{self.flight_plan_dir}\n{self.params_dir}")
    
    def open_main_window(self):
        """Open the main application window"""
        self.main = MainWindow(self.flight_plan_dir, self.params_dir)
        self.main.showMaximized()
        self.close()

    def apply_dark_theme(self):
        self.app.setStyle("Fusion")
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        self.app.setPalette(dark_palette)
        self.app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")