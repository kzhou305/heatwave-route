import os
from shapely.geometry import LineString, Point

def get_gsv_images(path):
    line = LineString(path['geometry']['coordinates'])
    images = []
    for root, _, files in os.walk("../data/gsv"):
        for f in files:
            if f.endswith(".jpg") and "Location_" in f:
                try:
                    coord = f.split("Location_")[1].split("-heading")[0]
                    lon, lat = map(float, coord.split(","))
                    if line.buffer(0.0002).contains(Point(lon, lat)):
                        images.append(f)
                except: continue
    return sorted(images)
