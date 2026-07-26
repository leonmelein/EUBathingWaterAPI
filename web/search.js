const submitBtn = document.getElementById('submit');
const locateBtn = document.getElementById('location');
const results = document.getElementById('results');

locateBtn.addEventListener('click', (e) => {
    if (navigator.geolocation) {
        console.log("Locate");
        navigator.geolocation.getCurrentPosition((position) => {
            console.log("Latitude:", position.coords.latitude);
            console.log("Longitude:", position.coords.longitude);
        });
    } else {
        console.log("Geolocation not supported");
    }
});

submitBtn.addEventListener('click', (e) => {
    let country = document.getElementById("country").value;
    let query = document.getElementById("query").value;

    

    results.insertAdjacentHTML('beforeend', `<li>Amsterdam</li>`)
})

console.log("Hello world");
