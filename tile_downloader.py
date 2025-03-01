import os
import requests
import threading
import math
from tqdm import tqdm

class TileDownloader:
    TILE_URL = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
    TILE_FOLDER = "tiles"
    THREADS = 10

    def __init__(self, zoom_level, x_range, y_range, threads=10):
        self.zoom_level = zoom_level
        self.x_range = x_range
        self.y_range = y_range
        self.THREADS = threads
        self.tasks = [(self.zoom_level, x, y) for x in self.x_range for y in self.y_range]
        self.lock = threading.Lock()

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

    def worker(self, pbar):
        """Worker thread to process download tasks."""
        while True:
            with self.lock:
                if not self.tasks:
                    break
                z, x, y = self.tasks.pop()
            
            self.download_tile(z, x, y)
            pbar.update(1)

    def download_tiles(self):
        """Download tiles using multithreading."""
        with tqdm(total=len(self.tasks)) as pbar:
            threads = [threading.Thread(target=self.worker, args=(pbar,)) for _ in range(self.THREADS)]
            
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

def lat_lon_to_tile(lat, lon, zoom):
    """Convert latitude, longitude, and zoom level to tile coordinates."""
    lat_rad = math.radians(lat)
    n = 2 ** zoom
    tile_x = n * (lon + 180) / 360
    tile_y = n * (1 - (math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi)) / 2
    return tile_x, tile_y

if __name__ == "__main__":
    min_lat = 43.875552
    max_lat = 43.881725
    min_lon = -79.418744
    max_lon = -79.405701
    
    for zoom_level in range(15, 20):
        top_left = lat_lon_to_tile(max_lat, min_lon, zoom_level)
        bottom_right = lat_lon_to_tile(min_lat, max_lon, zoom_level)
        
        x_range = range(math.floor(top_left[0]), math.ceil(bottom_right[0]))
        y_range = range(math.floor(top_left[1]), math.ceil(bottom_right[1]))
        
        downloader = TileDownloader(zoom_level, x_range, y_range, threads=10)
        downloader.download_tiles()