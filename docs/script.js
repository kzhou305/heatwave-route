let map = L.map('map').setView([35.6895, 139.6917], 14);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
let points = [];

map.on('click', function(e) {
  if (points.length >= 2) {
    points = [];
    map.eachLayer(layer => { if (layer._latlng) map.removeLayer(layer); });
  }
  points.push(e.latlng);
  L.marker(e.latlng).addTo(map);
});

function calculateRoute() {
  if (points.length < 2) {
    alert("Select two points");
    return;
  }

  // Placeholder: write custom routing algorithm here using pre-loaded GeoJSON graph
  L.polyline(points, { color: 'red' }).addTo(map);

  // Optional: generate buffer using Turf.js and find nearby GSV images
  const line = turf.lineString(points.map(p => [p.lng, p.lat]));
  const buffered = turf.buffer(line, 0.02, { units: 'kilometers' });
  L.geoJSON(buffered, { style: { color: 'blue', weight: 1, fillOpacity: 0.1 } }).addTo(map);

  // You can later intersect buffered area with image points loaded from CSV/GeoJSON
}
