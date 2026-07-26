import { Circle, CircleMarker, Control, FeatureGroup, GeoJSON, Layer, Map, TileLayer } from "https://unpkg.com/leaflet/dist/leaflet-src.esm.js";
import { addToLocalStorageArray, countriesByIso } from "./index.js";


const map = new Map("map", {
    zoomControl: true,
    preferCanvas: true
}).setView([54, 15], 6);

const dialog = document.getElementById('dialog');
const dialogClose = document.getElementById('closeDialog');
const attributionControl = map.attributionControl;
let loadStatusAttribution = "Loading GeoJSON...";

const countryColorsByIso: Record<string, string> = {
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

new TileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

setLoadStatus(loadStatusAttribution)
map.locate({ setView: true, maxZoom: 4 });

map.on('locationfound', (e) => {
    var radius = e.accuracy;
    new CircleMarker(e.latlng, {}).addTo(map)
    new Circle(e.latlng, radius).addTo(map);
});

dialogClose!.addEventListener('click', () => {
    dialog!.hidePopover();
});

function isoCodeToFlagEmoji(isoCode: string) {
    const code = isoCode.substring(0, 2)
    const flagIsoCode = { uk: "gb" }[code] ?? code;

    return flagIsoCode
        .toUpperCase()
        .replace(/./g, (char) => String.fromCodePoint(127397 + char.charCodeAt(0)));
}

function tooltipHtml(feature: any) {
    const props = feature?.properties ?? {};
    const name = props.name ?? "Unnamed location";

    return `<strong>${name}</strong>`;
}

function setLoadStatus(message: string) {
    if (screen.width > 768) {
        attributionControl.removeAttribution(loadStatusAttribution);
        loadStatusAttribution = message;
        attributionControl.addAttribution(loadStatusAttribution);
    }
}

async function loadCountryGeoJson(isoCode: string) {
    const path = `../data/${isoCode}/locations.geojson`;
    const response = await fetch(path);
    if (!response.ok) {
        throw new Error(`${response.status} ${response.statusText}`);
    }
    const geojson = await response.json();
    return { isoCode, path, geojson };
}

Promise.allSettled(Object.keys(countriesByIso).map((isoCode) => loadCountryGeoJson(isoCode)))
    .then((results) => {
        const overlays: Record<string, Layer> = {};
        const allLayers: Layer[] | undefined = [];
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
            const layer = new GeoJSON(geojson, {
                pointToLayer: (_, latlng) => new CircleMarker(latlng, {
                    radius: 6,
                    weight: 1,
                    color,
                    fillColor: color,
                    fillOpacity: 0.75
                }).on('click', (e) => {
                    dialog!.showPopover();
                    var properties = e.target.feature.properties;
                    document.getElementById("title")!.textContent = properties.name;
                    document.getElementById("country")!.textContent = `${isoCodeToFlagEmoji(properties.country)} ${countriesByIso[properties.country]}`
                    dialog!.getElementsByClassName('favorite')[0].addEventListener('click', () => {
                        addToLocalStorageArray('favorites', `${properties.country}\\${properties.id}`)
                    });
                }),
                onEachFeature: (feature, featureLayer) => {
                    featureLayer.bindTooltip(tooltipHtml(feature));
                }
            }).addTo(map);

            const count = Array.isArray(geojson.features) ? geojson.features.length : 0;
            totalCount += count;
            loadedLayers += 1;
            overlays[`${countriesByIso[isoCode]} (${count.toLocaleString()})`] = layer;
            allLayers.push(layer);
        });

        if (allLayers.length > 0) {
            const group = new FeatureGroup(allLayers);
            const bounds = group.getBounds();
            // const em = parseFloat(getComputedStyle(document.documentElement).fontSize);

            map.fitBounds(bounds.pad(0.05), {
                paddingTopLeft: [0, 20]   // 1em top padding
            });

            var layerControl = new Control.Layers(undefined, overlays, { collapsed: true }).addTo(map);
            map.removeControl(layerControl);
        }

        if (loadedLayers === 0) {
            throw new Error("No country GeoJSON files could be loaded");
        }

        setLoadStatus(`<span class="load-status">${totalCount.toLocaleString()} locations in ${loadedLayers} countries${failedLayers ? ` (${failedLayers} failed)</span>` : ""}`);
    })
    .catch((error) => {
        console.error(error);
        setLoadStatus(`Failed to load country GeoJSON layers: ${error.message}`);
    });
