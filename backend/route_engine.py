import networkx as nx
import geopandas as gpd
from shapely.geometry import Point

def build_graph():
    roads = gpd.read_file("../data/osm_roads.geojson")
    G = nx.Graph()
    for _, row in roads.iterrows():
        coords = list(row.geometry.coords)
        for i in range(len(coords) - 1):
            G.add_edge(coords[i], coords[i+1], weight=Point(coords[i]).distance(Point(coords[i+1])))
    return G

def find_route(G, start, end):
    start_pt = (start['lng'], start['lat'])
    end_pt = (end['lng'], end['lat'])
    s_node = min(G.nodes, key=lambda x: Point(x).distance(Point(start_pt)))
    e_node = min(G.nodes, key=lambda x: Point(x).distance(Point(end_pt)))
    path = nx.shortest_path(G, source=s_node, target=e_node, weight='weight')
    return {"type": "Feature", "geometry": {"type": "LineString", "coordinates": path}, "properties": {}}
