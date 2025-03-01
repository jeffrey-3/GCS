import os
import requests
import threading
from tqdm import tqdm

# OpenStreetMap tile URL template
TILE_URL = "https://a.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png"
TILE_FOLDER = "tiles"

# Define download range
ZOOM_LEVELS = range(15, 16)  # Change zoom range as needed
X_RANGE = range(9100, 9200)  # Adjust X tile range for the desired area
Y_RANGE = range(11900, 12000)  # Adjust Y tile range

# Number of threads for downloading
THREADS = 10

def download_tile(z, x, y):
    """Download a single tile and save it."""
    tile_path = os.path.join(TILE_FOLDER, str(z), str(x), f"{y}.png")
    
    if os.path.exists(tile_path):  # Skip if already downloaded
        return
    
    os.makedirs(os.path.dirname(tile_path), exist_ok=True)
    
    url = TILE_URL.format(z=z, x=x, y=y)
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(tile_path, "wb") as f:
                f.write(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")

def download_tiles():
    """Download tiles using multithreading."""
    tasks = [(z, x, y) for z in ZOOM_LEVELS for x in X_RANGE for y in Y_RANGE]

    with tqdm(total=len(tasks)) as pbar:
        def worker():
            while tasks:
                try:
                    z, x, y = tasks.pop()
                    download_tile(z, x, y)
                    pbar.update(1)
                except IndexError:
                    break  # No more tasks

        threads = [threading.Thread(target=worker) for _ in range(THREADS)]
        
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

if __name__ == "__main__":
    print("Starting tile download...")
    download_tiles()
    print("Download complete!")
