import sys
import io
import folium
from folium import plugins
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView

# py -m http.server 8000

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Folium in PyQt Example')
        self.window_width, self.window_height = 1600, 1200
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        coordinate = ()
        m = folium.Map(
        	tiles="http://localhost:8000/tiles/{z}/{x}/{y}.png", # It will reset when you comment, run, uncomment, then run again
        	zoom_start=15,
        	location=coordinate,
            attr="<a href=https://endless-sky.github.io/>Endless Sky</a>"
        )

        plane_position=  [43.8787, -79.41371]
        coordinates = [
            [43.878, -79.41371],
            plane_position
        ]
        line = folium.PolyLine(coordinates, color="red", opacity=0).add_to(m)
        attr = {"fill": "red", "font-weight": "bold", "font-size": "30"}
        plugins.PolyLineTextPath(line,
            "\u2708",  # Plane unicode symbol
            repeat=False,
            offset=14.5,
            orientation=180,
            attributes=attr).add_to(m)

        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)

        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        layout.addWidget(webView)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(1000)  # Update every second
    
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
    app.setStyleSheet('''
        QWidget {
            font-size: 35px;
        }
    ''')
    
    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')