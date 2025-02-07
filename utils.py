import math

def calculate_displacement_meters(lat, lon, center_lat, center_lon):
    # Earth's radius in meters
    R = 6378137.0
    
    # Convert degrees to radians
    center_lat_rad = math.radians(center_lat)
    center_lon_rad = math.radians(center_lon)
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    
    # Differences in coordinates
    delta_lat = lat_rad - center_lat_rad
    delta_lon = lon_rad - center_lon_rad
    
    # Approximate Cartesian coordinates
    east = R * delta_lon * math.cos((center_lat_rad + lat_rad) / 2)
    north = R * delta_lat
    
    return east, north