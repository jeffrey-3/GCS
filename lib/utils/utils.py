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

def calculate_bearing(point1, point2):
    """
    Calculate the bearing (angle) between two latitude/longitude points.
    :param point1: Tuple of (lat1, lon1) in degrees
    :param point2: Tuple of (lat2, lon2) in degrees
    :return: Bearing in degrees (0° to 360°)
    """
    lat1, lon1 = math.radians(point1[0]), math.radians(point1[1])
    lat2, lon2 = math.radians(point2[0]), math.radians(point2[1])

    dlon = lon2 - lon1

    x = math.sin(dlon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)

    bearing = math.atan2(x, y)
    bearing = math.degrees(bearing)
    bearing = (bearing + 360) % 360  # Normalize to 0-360°

    return bearing

def flatten_array(arr):
    flattened = []
    
    def recursive_flatten(element):
        if isinstance(element, list):
            for item in element:
                recursive_flatten(item)
        else:
            flattened.append(element)
    
    recursive_flatten(arr)
    return flattened