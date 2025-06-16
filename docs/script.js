let map = L.map('map').setView([35.6895, 139.6917], 14);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

let points = [];
let roadsGeojson;
let graph = new graphlib.Graph({ directed: false });

fetch("data/osm_roads.geojson")
  .then(res => res.json())
  .then(data => {
    roadsGeojson = data;
    buildGraph(data);
    L.geoJSON(data, { style: { color: "#aaa", weight: 1 } }).addTo(map);
  });

map.on('click', function (e) {
  if (points.length >= 2) {
    points = [];
    map.eachLayer(l => { if (l._latlng || l.feature) map.removeLayer(l); });
    L.geoJSON(roadsGeojson, { style: { color: "#aaa", weight: 1 } }).addTo(map);
  }
  points.push(e.latlng);
  L.marker(e.latlng).addTo(map);
});

function buildGraph(geojson) {
  geojson.features.forEach((f, idx) => {
    let coords = f.geometry.coordinates;
    for (let i = 0; i < coords.length - 1; i++) {
      let a = coords[i].join(",");
      let b = coords[i + 1].join(",");
      let dist = turf.distance(turf.point(coords[i]), turf.point(coords[i + 1]), { units: "kilometers" });
      graph.setEdge(a, b, dist);
    }
  });
}

function calculateRoute() {
  if (points.length < 2) return alert("Select two points");

  let start = findNearestNode(points[0]);
  let end = findNearestNode(points[1]);

  let path = graphlib.alg.dijkstra(graph, start);
  let current = end;
  let coords = [end.split(',').map(Number)];

  while (current !== start) {
    current = path[current].predecessor;
    if (!current) return alert("Path not found");
    coords.unshift(current.split(',').map(Number));
  }

  let latlngs = coords.map(c => [c[1], c[0]]);
  L.polyline(latlngs, { color: 'red' }).addTo(map);
}

function findNearestNode(latlng) {
  let minDist = Infinity;
  let nearest = null;
  graph.nodes().forEach(n => {
    let [lon, lat] = n.split(',').map(Number);
    let d = turf.distance(turf.point([lon, lat]), turf.point([latlng.lng, latlng.lat]));
    if (d < minDist) {
      minDist = d;
      nearest = n;
    }
  });
  return nearest;
}
