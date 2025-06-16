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

function getRoute() {
  if (points.length < 2) return alert("Select 2 points");
  fetch('/route', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ start: points[0], end: points[1] })
  }).then(res => res.json()).then(data => {
    L.geoJSON(data.route).addTo(map);
  });
}
