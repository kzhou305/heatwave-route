let points = [];
map.on('click', function(e) {
  if (points.length >= 2) points = [];
  points.push(e.latlng);
  L.marker(e.latlng).addTo(map);
});

function sendRequest() {
  fetch("/route", {
    method: "POST",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ start: points[0], end: points[1] })
  })
  .then(res => res.json())
  .then(data => L.geoJSON(data.route).addTo(map));
}
