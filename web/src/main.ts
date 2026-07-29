import L, { Circle, CircleMarker, DivIcon, GeoJSON, latLngBounds, Map as LeafletMap, Marker, TileLayer } from 'leaflet';
import 'leaflet.markercluster';
import { addToLocalStorageArray, countriesByIso, countryColorsByIso, isInLocalStorageArray, isoCodeToFlagEmoji } from './country';

type CountryIndexEntry = {
    iso: string;
    name: string;
    count: number;
    geojson: string;
    bounds: [[number, number], [number, number]] | null;
};

const dialog = document.getElementById('dialog');
const dialogClose = document.getElementById('closeDialog');
dialogClose!.addEventListener('click', () => {
    dialog!.hidePopover();
});

function mapSetup(){
    let loadStatusAttribution = "Loading GeoJSON...";

    const map = new LeafletMap("map", {
        zoomControl: true,
        preferCanvas: true
    }).setView([54, 15], 6);
    const attributionControl = map.attributionControl;


    new TileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);
    const clusterGroup = L.markerClusterGroup({
        chunkedLoading: true,
        chunkInterval: 50,
        chunkDelay: 25,
        showCoverageOnHover: false,
        removeOutsideVisibleBounds: true,
        disableClusteringAtZoom: 13,
    }).addTo(map);

    attributionControl.addAttribution(loadStatusAttribution);
    map.locate({ setView: true, maxZoom: 4 });

    map.on('locationfound', (e) => {
        var radius = e.accuracy;
        new CircleMarker(e.latlng, {}).addTo(map)
        new Circle(e.latlng, radius).addTo(map);
    });

    loadCountryIndex()
        .then((countries) => {
            const loadPromises = new Map<string, Promise<void>>();
            const loadedCountries = new Set<string>();
            const failedCountries = new Set<string>();
            const countryCountMarkers = new Map<string, Marker>();
            const totalCount = countries.reduce((count, country) => count + country.count, 0);

            const countriesWithBounds = countries.filter((country) => country.bounds);
            if (countriesWithBounds.length > 0) {
                const bounds = latLngBounds(countriesWithBounds[0].bounds!);
                countriesWithBounds.slice(1).forEach((country) => bounds.extend(country.bounds!));
                map.fitBounds(bounds.pad(0.05), {
                    paddingTopLeft: [0, 20]   // 1em top padding
                });
            }

            countriesWithBounds.forEach((country) => {
                const marker = new Marker(countryCenter(country), {
                    icon: new DivIcon({
                        className: "country-count-marker",
                        html: `<span>${country.count.toLocaleString()}</span>`,
                    }),
                    title: `${country.name}: ${country.count.toLocaleString()} spots`,
                }).addTo(map);

                marker.on("click", () => {
                    map.fitBounds(latLngBounds(country.bounds!), {
                        maxZoom: 7,
                        padding: [24, 24],
                    });
                });

                countryCountMarkers.set(country.iso, marker);
            });

            const updateLoadStatus = () => {
                if (screen.width <= 768) {
                    return;
                }

                attributionControl.removeAttribution(loadStatusAttribution);
                loadStatusAttribution = `<span class="load-status">${loadedCountries.size.toLocaleString()} of ${countries.length.toLocaleString()} countries loaded (${totalCount.toLocaleString()} locations available)${failedCountries.size ? `, ${failedCountries.size} failed</span>` : "</span>"}`;
                attributionControl.addAttribution(loadStatusAttribution);
            };

            const loadVisibleCountries = () => {
                if (map.getZoom() < 7) {
                    updateLoadStatus();
                    return;
                }

                const mapBounds = map.getBounds();
                countries.forEach((country) => {
                    if (!country.bounds || loadedCountries.has(country.iso) || loadPromises.has(country.iso)) {
                        return;
                    }

                    if (!mapBounds.intersects(latLngBounds(country.bounds))) {
                        return;
                    }

                    const loadPromise = loadCountryGeoJson(country)
                        .then(({ geojson }) => {
                            const color = countryColorsByIso[country.iso] ?? "#0f766e";
                            const geoJsonLayer = new GeoJSON(geojson, {
                                pointToLayer: (feature, latlng) => {
                                    const marker = new Marker(latlng, {
                                        icon: new DivIcon({
                                            className: "location-marker",
                                            html: `<span style="--marker-color: ${color}"></span>`,
                                        }),
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
                            });

                            clusterGroup.addLayer(geoJsonLayer);

                            loadedCountries.add(country.iso);
                            countryCountMarkers.get(country.iso)?.remove();
                            countryCountMarkers.delete(country.iso);
                        })
                        .catch((error) => {
                            failedCountries.add(country.iso);
                            console.error(`Failed to load ${country.iso} GeoJSON`, error);
                        })
                        .finally(() => {
                            loadPromises.delete(country.iso);
                            updateLoadStatus();
                        });

                    loadPromises.set(country.iso, loadPromise);
                });

                updateLoadStatus();
            };

            map.on('moveend zoomend', loadVisibleCountries);
            loadVisibleCountries();
        })
        .catch((error) => {
            console.error(error);
            if (screen.width > 768) {
                attributionControl.removeAttribution(loadStatusAttribution);
                loadStatusAttribution = `Failed to load country index: ${error.message}`;
                attributionControl.addAttribution(loadStatusAttribution);
            }
    });
}

function tooltipHtml(feature: any) {
    const props = feature?.properties ?? {};
    const name = props.name ?? "Unnamed location";

    return `<strong>${name}</strong>`;
}

function countryCenter(country: CountryIndexEntry): [number, number] {
    const [[south, west], [north, east]] = country.bounds!;
    return [(south + north) / 2, (west + east) / 2];
}

async function loadCountryIndex(): Promise<CountryIndexEntry[]> {
    const response = await fetch("/data/countries.json");
    if (!response.ok) {
        throw new Error(`${response.status} ${response.statusText}`);
    }

    return response.json();
}

async function loadCountryGeoJson(country: CountryIndexEntry) {
    const path = country.geojson.startsWith("/") ? country.geojson : `/${country.geojson}`;
    const response = await fetch(path);
    if (!response.ok) {
        throw new Error(`${response.status} ${response.statusText}`);
    }
    const geojson = await response.json();
    return { path, geojson };
}

mapSetup();
