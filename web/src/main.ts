import { Circle, CircleMarker, FeatureGroup, GeoJSON, Layer, Map, TileLayer } from 'leaflet';
import { addToLocalStorageArray, countriesByIso, countryColorsByIso, isInLocalStorageArray, isoCodeToFlagEmoji } from './country';

const dialog = document.getElementById('dialog');
const dialogClose = document.getElementById('closeDialog');
dialogClose!.addEventListener('click', () => {
    dialog!.hidePopover();
});

function mapSetup(){
    let loadStatusAttribution = "Loading GeoJSON...";

    const map = new Map("map", {
        zoomControl: true,
        preferCanvas: true
    }).setView([54, 15], 6);
    const attributionControl = map.attributionControl;


    new TileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    attributionControl.addAttribution(loadStatusAttribution);
    map.locate({ setView: true, maxZoom: 4 });

    map.on('locationfound', (e) => {
        var radius = e.accuracy;
        new CircleMarker(e.latlng, {}).addTo(map)
        new Circle(e.latlng, radius).addTo(map);
    });

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
                    pointToLayer: (feature, latlng) => {
                        const marker = new CircleMarker(latlng, {
                            radius: 6,
                            weight: 1,
                            color,
                            fillColor: color,
                            fillOpacity: 0.75
                        });

                        marker.on('mouseover', () => {
                            if (!marker.getTooltip()) {
                                marker.bindTooltip(tooltipHtml(feature));
                            }

                            marker.openTooltip();
                        });

                        marker.on('click', (e) => {
                            dialog!.showPopover();
                            var properties = e.target.feature.properties;
                            document.getElementById("title")!.textContent = properties.name;
                            document.getElementById("country")!.textContent = `${isoCodeToFlagEmoji(properties.country)} ${countriesByIso[properties.country]}`

                            const favoriteButton = dialog!.getElementsByClassName('favorite')[0] as HTMLElement;
                            const favoriteId = `${properties.country}/${properties.id}`;

                            if (isInLocalStorageArray('favorites', favoriteId)) {
                                favoriteButton.innerHTML = `<span class="icon">✅</span><p>Added to favorites`;
                            } else {
                                favoriteButton.innerHTML = `<span class="icon">♥️</span><p>Add to favorites`;
                            }

                            favoriteButton.onclick = () => {
                                addToLocalStorageArray('favorites', `${properties.country}/${properties.id}`)
                                favoriteButton.innerHTML = `<span class="icon">✅</span><p>Added to favorites`
                            };
                        });

                        return marker;
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

            map.fitBounds(bounds.pad(0.05), {
                paddingTopLeft: [0, 20]   // 1em top padding
            });
        }

        if (loadedLayers === 0) {
            throw new Error("No country GeoJSON files could be loaded");
        }

        if (screen.width > 768) {
            attributionControl.removeAttribution(loadStatusAttribution);
            loadStatusAttribution = `<span class="load-status">${totalCount.toLocaleString()} locations in ${loadedLayers} countries${failedLayers ? ` (${failedLayers} failed)</span>` : ""}`;
            attributionControl.addAttribution(loadStatusAttribution);
        }
    })
        .catch((error) => {
            console.error(error);
            if (screen.width > 768) {
                attributionControl.removeAttribution(loadStatusAttribution);
                loadStatusAttribution = `Failed to load country GeoJSON layers: ${error.message}`;
                attributionControl.addAttribution(loadStatusAttribution);
            }
    });
}

function tooltipHtml(feature: any) {
    const props = feature?.properties ?? {};
    const name = props.name ?? "Unnamed location";

    return `<strong>${name}</strong>`;
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

mapSetup();
