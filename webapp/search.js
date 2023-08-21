import { sortByDistance } from "./sort.js"; 

let countries;
let search_term = '';

const search_input = document.getElementById('search');

const fetchCountries = async () => {
    countries = await fetch(
        'http://localhost:5500/locations.geojson'
    ).then(res => res.json());
};

const showCountries = async () => {
    const ul = document.getElementById('resultlist');
    ul.innerHTML = '';

    // getting the data
    await fetchCountries();
    let data = countries['features']
    sortByDistance(data, 4.836666, 52.3641429)

    var items = data.filter(item =>
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
