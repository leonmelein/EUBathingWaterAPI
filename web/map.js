const statusEl = document.getElementById("status");
const map = L.map("map", {
    zoomControl: true,
    preferCanvas: true
}).setView([54, 15], 6);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);
map.locate({ setView: true, maxZoom: 4 });

const countryCodes = [
    "al", "at", "be", "bg", "cy", "cz", "de", "dk", "ee", "es", "fr", "fi", "gr", "hr", "hu", "ie", "it", "lt", "lu", "lv", "mt", "nl", "pl", "pt", "ro", "se", "sk", "si", "ch", "uk"
];

const countriesByIso = {
    al: "Albania",
    at: "Austria",
    be: "Belgium",
    bg: "Bulgaria",
    cy: "Cyprus",
    cz: "Czechia",
    de: "Germany",
    dk: "Denmark",
    ee: "Estonia",
    es: "Spain",
    fr: "France",
    fi: "Finland",
    gr: "Greece",
    hr: "Croatia",
    hu: "Hungary",
    ie: "Ireland",
    it: "Italy",
    lt: "Lithuania",
    lu: "Luxembourg",
    lv: "Latvia",
    mt: "Malta",
    nl: "Netherlands",
    pl: "Poland",
    pt: "Portugal",
    ro: "Romania",
    se: "Sweden",
    si: "Slovenia",
    sk: "Slovakia",
    ch: "Switzerland",
    uk: "United Kingdom"
};


function onLocationFound(e) {
    var radius = e.accuracy;
    L.marker(e.latlng).addTo(map)
    L.circle(e.latlng, radius).addTo(map);
}

map.on('locationfound', onLocationFound);

async function loadCountryGeoJson(isoCode) {
    const path = `../data/${isoCode}/locations.geojson`;
    const response = await fetch(path);
    if (!response.ok) {
        throw new Error(`${response.status} ${response.statusText}`);
    }
    const geojson = await response.json();
    return { isoCode, path, geojson };
}

function popupHtml(feature) {
    const props = feature?.properties ?? {};
    const name = props.name ?? "Unnamed location";
    const extra = Object.entries(props)
        .filter(([key]) => key !== "name")
        .slice(0, 6)
        .map(([key, value]) => `<div><strong>${key}</strong>: ${String(value)}</div>`)
        .join("");

    return `<div><strong>${name}</strong>${extra ? `<hr>${extra}` : ""}</div>`;
}

Promise.allSettled(countryCodes.map((isoCode) => loadCountryGeoJson(isoCode)))
    .then((results) => {
        const palette = ["#0f766e", "#0369a1", "#1d4ed8", "#6d28d9", "#b91c1c", "#15803d", "#854d0e"];
        const overlays = {};
        const allLayers = [];
        let loadedLayers = 0;
        let failedLayers = 0;
        let totalCount = 0;

        results.forEach((result, index) => {
            if (result.status !== "fulfilled") {
                failedLayers += 1;
                return;
            }

            const { isoCode, geojson } = result.value;
            const color = palette[index % palette.length];
            const layer = L.geoJSON(geojson, {
                pointToLayer: (_, latlng) => L.circleMarker(latlng, {
                    radius: 4,
                    weight: 1,
                    color,
                    fillColor: color,
                    fillOpacity: 0.75
                }),
                onEachFeature: (feature, featureLayer) => {
                    featureLayer.bindPopup(popupHtml(feature), { maxWidth: 280 });
                }
            }).addTo(map);

            const count = Array.isArray(geojson.features) ? geojson.features.length : 0;
            totalCount += count;
            loadedLayers += 1;
            overlays[`${countriesByIso[isoCode]} (${count.toLocaleString()})`] = layer;
            allLayers.push(layer);
        });

        if (allLayers.length > 0) {
            const group = L.featureGroup(allLayers);
            const bounds = group.getBounds();
            const em = parseFloat(getComputedStyle(document.documentElement).fontSize);

            map.fitBounds(bounds.pad(0.05), {
                paddingTopLeft: [0, em]   // 1em top padding
            });

            L.control.layers(null, overlays, { collapsed: true }).addTo(map);
        }

        if (loadedLayers === 0) {
            throw new Error("No country GeoJSON files could be loaded");
        }

        statusEl.textContent = `Loaded ${totalCount.toLocaleString()} locations from ${loadedLayers} countries${failedLayers ? ` (${failedLayers} failed)` : ""}`;
    })
    .catch((error) => {
        console.error(error);
        statusEl.textContent = `Failed to load country GeoJSON layers: ${error.message}`;
        statusEl.classList.add("status-error");
    });