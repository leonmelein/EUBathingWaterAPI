const map = L.map("map", {
    zoomControl: true,
    preferCanvas: true
}).setView([54, 15], 6);
const attributionControl = map.attributionControl;
let loadStatusAttribution = "Loading GeoJSON...";

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);
attributionControl.addAttribution(loadStatusAttribution);
map.locate({ setView: true, maxZoom: 4 });

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

const countryColorsByIso = {
    al: "#da291c",
    at: "#ed2939",
    be: "#b31b34",
    bg: "#00966e",
    cy: "#d57800",
    cz: "#11457e",
    de: "#000000",
    dk: "#c60c30",
    ee: "#4891d9",
    es: "#aa151b",
    fr: "#0055a4",
    fi: "#003580",
    gr: "#0d5eaf",
    hr: "#cf1020",
    hu: "#436f4d",
    ie: "#169b62",
    it: "#009246",
    lt: "#fdb913",
    lu: "#00a3e0",
    lv: "#9e3039",
    mt: "#cf142b",
    nl: "#b85c00",
    pl: "#dc143c",
    pt: "#046a38",
    ro: "#002b7f",
    se: "#006aa7",
    si: "#005da4",
    sk: "#0b4ea2",
    ch: "#d52b1e",
    uk: "#012169"
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

function setLoadStatus(message) {
    attributionControl.removeAttribution(loadStatusAttribution);
    loadStatusAttribution = message;
    attributionControl.addAttribution(loadStatusAttribution);
}

Promise.allSettled(Object.keys(countriesByIso).map((isoCode) => loadCountryGeoJson(isoCode)))
    .then((results) => {
        const overlays = {};
        const allLayers = [];
        let loadedLayers = 0;
        let failedLayers = 0;
        let totalCount = 0;

        results.forEach((result) => {
            if (result.status !== "fulfilled") {
                failedLayers += 1;
                return;
            }

            const { isoCode, geojson } = result.value;
            const color = countryColorsByIso[isoCode] ?? "#0f766e";
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
                paddingTopLeft: [0, 20]   // 1em top padding
            });

            L.control.layers(null, overlays, { collapsed: true }).addTo(map);
        }

        if (loadedLayers === 0) {
            throw new Error("No country GeoJSON files could be loaded");
        }

        setLoadStatus(`${totalCount.toLocaleString()} locations in ${loadedLayers} countries${failedLayers ? ` (${failedLayers} failed)` : ""}`);
    })
    .catch((error) => {
        console.error(error);
        setLoadStatus(`Failed to load country GeoJSON layers: ${error.message}`);
    });
