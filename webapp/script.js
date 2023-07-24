mapboxgl.accessToken =
  "pk.eyJ1IjoidGhlc29jaWFsbGlvbnMiLCJhIjoiY2xqdnJyeWZuMHI5bzNmbnZ4YWFzMG8zZiJ9.UxvouECcaKRYO2quoReT6g";

this.map = new mapboxgl.Map({
  container: "map", // container id
  style: "mapbox://styles/mapbox/streets-v9",
  center: [5.3835819, 52.1556708], // starting position
  zoom: 7 // starting zoom
});

// Add zoom and rotation controls to the map.
var nav = new mapboxgl.NavigationControl();
map.addControl(nav, "top-right");

map.on("load", function () {
    map.resize()
    map.addSource("swimming", {
        type: "geojson",
        // Use a URL for the value for the `data` property.
        data:
        "http://127.0.0.1:8000/"
    });

    map.addLayer({
        id: "swim",
        type: "circle",
        source: "swimming",
        paint: {
        "circle-radius": 5,
        "circle-color": "#ff0000"
        }
    });
});

