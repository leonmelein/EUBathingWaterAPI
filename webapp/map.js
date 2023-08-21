var map = new maplibregl.Map({
  container: "map", // container id
    style: "/webapp/bright.json",
    center: [13.404954, 52.520008], // starting position
  zoom: 3 // starting zoom
});

// Add zoom and rotation controls to the map.
var nav = new maplibregl.NavigationControl();
map.addControl(nav, "top-right");

map.on("load", function () {
    map.addSource("swimming", {
        type: "geojson",
        // Use a URL for the value for the `data` property.
        data:
        "/locations.geojson"
    });

    map.addLayer({
        id: "swim",
        type: "circle",
        source: "swimming",
        paint: {
        "circle-radius": 5,
        "circle-color": "#5390E9"
        }
    });
    map.resize()

    map.addControl(
        new maplibregl.GeolocateControl({
            positionOptions: {
                enableHighAccuracy: true
            },
            trackUserLocation: true
        })
    )
});

