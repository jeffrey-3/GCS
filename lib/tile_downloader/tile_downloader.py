import os
import requests
import threading
import math
from tqdm import tqdm

class TileDownloader:
    TILE_URL = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
    TILE_FOLDER = "tiles"
    THREADS = 10

    def __init__(self, threads=10):
        self.THREADS = threads
        self.lock = threading.Lock()

    @staticmethod
    def lat_lon_to_tile(lat, lon, zoom):
        """Convert latitude, longitude, and zoom level to tile coordinates."""
        lat_rad = math.radians(lat)
        n = 2 ** zoom
        tile_x = n * (lon + 180) / 360
        tile_y = n * (1 - (math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi)) / 2
        return tile_x, tile_y

    def download_tile(self, z, x, y):
        """Download a single tile and save it."""
        tile_path = os.path.join(self.TILE_FOLDER, str(z), str(x), f"{y}.png")
        
        if os.path.exists(tile_path):  # Skip if already downloaded
            return
        
        os.makedirs(os.path.dirname(tile_path), exist_ok=True)
        
        url = self.TILE_URL.format(z=z, x=x, y=y)
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(tile_path, "wb") as f:
                    f.write(response.content)
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {url}: {e}")

    def worker(self, tasks, pbar):
        """Worker thread to process download tasks."""
        while True:
            with self.lock:
                if not tasks:
                    break
                z, x, y = tasks.pop()
            
            self.download_tile(z, x, y)
            pbar.update(1)

    def download_tiles_for_zoom(self, zoom_level, min_lat, max_lat, min_lon, max_lon):
        """Download tiles for a specific zoom level."""
        top_left = self.lat_lon_to_tile(max_lat, min_lon, zoom_level)
        bottom_right = self.lat_lon_to_tile(min_lat, max_lon, zoom_level)
        
        x_range = range(math.floor(top_left[0]), math.ceil(bottom_right[0]))
        y_range = range(math.floor(top_left[1]), math.ceil(bottom_right[1]))
        
        tasks = [(zoom_level, x, y) for x in x_range for y in y_range]
        
        with tqdm(total=len(tasks), desc=f"Downloading zoom level {zoom_level}") as pbar:
            threads = [threading.Thread(target=self.worker, args=(tasks, pbar)) for _ in range(self.THREADS)]
            
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

    def download_all_tiles(self, min_lat, max_lat, min_lon, max_lon, min_zoom, max_zoom):
        """Download tiles for all specified zoom levels."""
        for zoom_level in range(min_zoom, max_zoom + 1):
            self.download_tiles_for_zoom(zoom_level, min_lat, max_lat, min_lon, max_lon)