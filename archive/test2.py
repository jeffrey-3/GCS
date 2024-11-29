import sys
from offline_folium import offline
import folium
from PyQt5 import QtWidgets, QtWebEngineWidgets
from PyQt5.QtWidgets import *
sites/view/hunterwealth
icon = folium.CustomIcon(
    "mark.png",
    icon_size=(50, 50)
)

app = QtWidgets.QApplication(sys.argv)
map = folium.Map(location=[43.8787124, -79.4137864], 
                zoom_start=19, 
                max_zoom=19, 
                tiles="Esri.WorldImagery", 
                attributionControl=0, 
                zoom_control=0)

folium.Marker(
    location=[43.8787124, -79.4137864], 
    icon=icon
).add_to(map)

w = QtWebEngineWidgets.QWebEngineView()
w.setHtml(map.get_root().render())

window = QWidget()
layout = QHBoxLayout()
layout.setContentsMargins(0, 0, 0, 0)
layout.addWidget(QPushButton("Home"), 1)
layout.addWidget(w, 2)
window.setLayout(layout)

window.showFullScreen()
window.show()
sys.exit(app.exec_())