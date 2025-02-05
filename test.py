import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt

class GPSGrid(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        grid_layout = QGridLayout()

        for row in range(3):
            for col in range(3):
                # Create a vertical layout for each cell
                vbox = QVBoxLayout()
                vbox.setSpacing(2)  # Reduce space between labels

                # Small label (description)
                label_small = QLabel("Satellites", self)
                label_small.setStyleSheet("font-size: 10px;")  
                label_small.setAlignment(Qt.AlignCenter)  # Center text
                label_small.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

                # Large label (number)
                label_large = QLabel(f"{(row * 3) + col + 1}", self)
                label_large.setStyleSheet("font-size: 24px; font-weight: bold;")
                label_large.setAlignment(Qt.AlignCenter)  
                label_large.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

                # Add labels to the vertical layout
                vbox.addWidget(label_small)
                vbox.addWidget(label_large)
                vbox.setAlignment(Qt.AlignCenter)  # Align everything in the center

                # Add vertical layout to grid
                grid_layout.addLayout(vbox, row, col)

        self.setLayout(grid_layout)
        self.setWindowTitle("GPS Satellites Grid")
        # self.showFullScreen()  # Start in fullscreen mode
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GPSGrid()
    sys.exit(app.exec_())
