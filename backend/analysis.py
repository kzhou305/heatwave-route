from shapely.geometry import LineString, Point
import os

def match_gsv_images(route_coords, gsv_dir="../data/gsv"):
    buffer_line = LineString(route_coords).buffer(0.0002)
    matched = []
    for root, _, files in os.walk(gsv_dir):
        for file in files:
            if file.endswith(".jpg") and "Location_" in file:
                coord_part = file.split("Location_")[1].split("-heading")[0]
                lon, lat = map(float, coord_part.split(","))
                if buffer_line.contains(Point(lon, lat)):
                    matched.append((file, lon, lat))
    return matched
