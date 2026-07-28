import { countriesByIso, isoCodeToFlagEmoji } from "./country.ts";

// Load favorites
async function fetchData(item: string) {
    try {
        const response = await fetch(`/data/${item.split('/')[0]}/locations/${item.split('/')[1]}.json`);
        const data = await response.json();
        console.log(data);
        return data;
    } catch (error) {
        console.error('Error:', error);
    }
}

// Get LocalStorage items
const existing = localStorage.getItem('favorites');
const items = existing ? JSON.parse(existing) : [];
console.log(items);

// Loop through all and pull results
Promise.all(items.map(async (item: string) => {
    var data = await fetchData(item);
    console.log(data, data.name, data.country);
    console.log(typeof(data.name))

    const template = document.getElementById("favorite");

    if (template instanceof HTMLTemplateElement) {
        const fragment = template.content.cloneNode(true) as DocumentFragment;

        const titleSlot = fragment.getElementById("title") as HTMLSlotElement;
        const countrySlot = fragment.getElementById("country") as HTMLSlotElement;

        titleSlot.textContent = data.name;
        countrySlot.textContent = `${isoCodeToFlagEmoji(data.country)} ${countriesByIso[data.country]}`;

        document.querySelector(".favorites")!.appendChild(fragment);
    }
}));
// console.log(results);


// Display results