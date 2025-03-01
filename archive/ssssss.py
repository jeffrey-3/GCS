import sys
import io
import json
import folium
from folium import plugins
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Real-Time Plane Tracking')
        self.setMinimumSize(1600, 1200)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.coordinate = [43.8787, -79.41371]  # Initial position
        self.map = self.create_map(self.coordinate)

        # Save map to HTML
        data = io.BytesIO()
        self.map.save(data, close_file=False)

        # Web View
        self.webView = QWebEngineView()
        self.webView.setHtml(data.getvalue().decode())
        layout.addWidget(self.webView)

        # Timer for updating position
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(1000)  # Update every second

    def create_map(self, coordinate):
        """Create the Folium map with an initial plane position."""
        m = folium.Map(
            # tiles="http://localhost:8000/tiles/{z}/{x}/{y}.png",
            zoom_start=15,
            location=coordinate,
            attr="<a href=https://endless-sky.github.io/>Endless Sky</a>"
        )

        # Initial plane position
        line = folium.PolyLine([coordinate, coordinate], color="red", opacity=0).add_to(m)
        attr = {"fill": "red", "font-weight": "bold", "font-size": "30"}
        plugins.PolyLineTextPath(
            line, "\u2708", repeat=False, offset=14.5, orientation=180, attributes=attr
        ).add_to(m)

        return m

    def update_position(self):
        """Simulate real-time position updates and inject JavaScript."""
        # Simulating new position (e.g., moving slightly north)
        self.coordinate[0] += 0.0001  

        # JavaScript to move the plane
        js_code = f"""
        var newLatLng = [{self.coordinate[0]}, {self.coordinate[1]}];
        var planeIcon = document.querySelector("path.leaflet-interactive");
        if (planeIcon) {{
            planeIcon.setAttribute("d", "M " + newLatLng[1] + " " + newLatLng[0]);
        }}
        """

        # Run JavaScript in QWebEngineView to update plane position
        self.webView.page().runJavaScript(js_code)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('QWidget { font-size: 35px; }')

    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
