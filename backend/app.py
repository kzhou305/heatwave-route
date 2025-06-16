from flask import Flask, request, jsonify
from route_engine import build_graph, find_route
from gsv_fetcher import get_gsv_images

app = Flask(__name__)
G = build_graph()

@app.route('/route', methods=['POST'])
def route():
    data = request.get_json()
    path = find_route(G, data['start'], data['end'])
    gsv = get_gsv_images(path)
    return jsonify({'route': path, 'images': gsv})

if __name__ == '__main__':
    app.run(debug=True)
