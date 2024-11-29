import sys
from offline_folium import offline
import folium
from PyQt5 import QtWidgets, QtWebEngineWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

app = QtWidgets.QApplication(sys.argv)

mark_label = QLabel()
mark_label.setPixmap(QPixmap("mark.png").scaledToWidth(50))

map = folium.Map(location=[43.8787124, -79.4137864], 
                zoom_start=19, 
                max_zoom=19, 
                tiles="Esri.WorldImagery", 
                attributionControl=0, 
                zoom_control=0,
                scrollWheelZoom=False,
                dragging=False)

w = QtWebEngineWidgets.QWebEngineView()
w.setHtml(map.get_root().render())
vfv vgro znq
window = QWidget()
map_layout = QGridLayout()
map_layout.addWidget(w, 0, 0)
map_layout.addWidget(mark_label, 0, 0, alignment=Qt.AlignCenter)
layout = QHBoxLayout()
layout.addWidget(QPushButton("Test Button"), 1)
layout.addLayout(map_layout, 2)
layout.setContentsMargins(0, 0, 0, 0)
window.setLayout(layout)

window.showFullScreen()
window.show()
sys.exit(app.exec_())