import staticmap
import math
import json

def lat_lon_to_meters_per_pixel(lat, zoom):
    """
    Calculate meters per pixel at a given latitude and zoom level.
    """
    EARTH_CIRCUMFERENCE = 40075016.686  # in meters
    TILE_SIZE = 256  # standard tile size
    
    # Calculate the resolution (meters per pixel)
    meters_per_pixel = EARTH_CIRCUMFERENCE * abs(math.cos(math.radians(lat))) / (2 ** zoom * TILE_SIZE)
    return meters_per_pixel

def download_map(lat, lon, zoom, width, height):
    """
    Download a static map image and calculate the real-world width and height in meters.
    """
    # Create a static map with OpenStreetMap provider
    m = staticmap.StaticMap(width, height, url_template="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}")
    
    # Add a marker for the center location
    marker = staticmap.CircleMarker((lon, lat), "red", 0)
    m.add_marker(marker)
    
    # Render the map
    image = m.render(zoom)
    
    # Calculate real-world dimensions
    meters_per_pixel = lat_lon_to_meters_per_pixel(lat, zoom)
    map_width_meters = width * meters_per_pixel
    map_height_meters = height * meters_per_pixel
    
    print(f"Approximate map width: {map_width_meters:.2f} meters")
    print(f"Approximate map height: {map_height_meters:.2f} meters")
    
    # Save image
    output_filename = f"map/map_{int(lat*1e7)}_{int(lon*1e7)}_{int(map_width_meters*1e3)}_{int(map_height_meters*1e3)}.png"
    print(output_filename)
    image.save(output_filename)
    print(f"Map saved to {output_filename}")

# Example usage
if __name__ == "__main__":
    zoom_level = 15
    img_width = 100 # pixels
    img_height = 100  # pixels

    # Generate image for each waypoint
    file = open("examples/flight_plan/plan_2025_02_10_14_28_48.json", "r")
    waypoints = json.load(file)['waypoints']
    for waypoint in waypoints:
        download_map(waypoint['lat'], waypoint['lon'], zoom_level, img_width, img_height)