from app.utils.tile_downloader import TileDownloader

class TilesModel:
    def __init__(self):
        return

    def download(self, top_left_lat, top_left_lon, bottom_right_lat, bottom_right_lon, min_zoom, max_zoom):
        downloader = TileDownloader(threads=10)
        downloader.download_all_tiles((top_left_lat, top_left_lon), 
                                      (bottom_right_lat, bottom_right_lon), 
                                      min_zoom, 
                                      max_zoom)

        # QMessageBox.information(self, "Status", "Completed download")