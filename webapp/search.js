import { getDistance } from "./sort.js"; 

let countries;
let search_term = '';

const search_input = document.getElementById('search');

const fetchCountries = async () => {
    countries = await fetch(
        '/locations.geojson'
    ).then(res => res.json());
};

const showCountries = async () => {
    const ul = document.getElementById('resultlist');
    ul.innerHTML = '';

    // getting the data
    await fetchCountries();
    let data = countries['features']
    const lat = 52.3641429
    const lon = 4.836666

    let sortedData = data.sort((a, b) => {
        const distanceToA = getDistance(lat, lon, a.geometry.coordinates[1], a.geometry.coordinates[0]);
        const distanceToB = getDistance(lat, lon, b.geometry.coordinates[1], b.geometry.coordinates[0]);
        return distanceToA - distanceToB;
    })

    var items = sortedData.filter(item =>
        item.properties.name.toLowerCase().includes(search_term.toLowerCase())
    )

    items.forEach(item => {
        const li = document.createElement('li');
        li.textContent = item['properties']['name']
        ul.appendChild(li);
    });
};

// display initial countries
showCountries();

search_input.addEventListener('input', e => {
    // saving the input value
    search_term = e.target.value;

    // re-displaying countries based on the new search_term
    showCountries();
});
