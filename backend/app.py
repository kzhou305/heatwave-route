from flask import Flask, request, jsonify
from shapely.geometry import shape, Point
import geopandas as gpd
import networkx as nx
import json

app = Flask(__name__)
roads = gpd.read_file("../data/osm_roads.geojson")
G = nx.Graph()

# Build the graph
for _, row in roads.iterrows():
    coords = list(row.geometry.coords)
    for i in range(len(coords)-1):
        a, b = coords[i], coords[i+1]
        G.add_edge(a, b, weight=Point(a).distance(Point(b)))

@app.route("/route", methods=["POST"])
def route():
    data = request.get_json()
    start_pt = (data['start']['lng'], data['start']['lat'])
    end_pt = (data['end']['lng'], data['end']['lat'])

    s_node = min(G.nodes, key=lambda n: Point(n).distance(Point(start_pt)))
    e_node = min(G.nodes, key=lambda n: Point(n).distance(Point(end_pt)))

    path = nx.shortest_path(G, source=s_node, target=e_node, weight='weight')
    line = {"type": "LineString", "coordinates": path}
    return jsonify({"route": {"type": "Feature", "geometry": line, "properties": {}}})

if __name__ == '__main__':
    app.run(debug=True)
