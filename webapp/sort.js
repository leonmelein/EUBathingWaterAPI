export function getDistance(lat1, lon1, lat2, lon2) {
    const R = 6371e3; // Earth's radius in meters
    const φ1 = lat1 * Math.PI / 180; // Latitude of first point converted to radians
    const φ2 = lat2 * Math.PI / 180; // Latitude of second point converted to radians
    const Δφ = (lat2 - lat1) * Math.PI / 180; // Change in latitude converted to radians
    const Δλ = (lon2 - lon1) * Math.PI / 180; // Change in longitude converted to radians

    const a = Math.sin(Δφ / 2) * Math.sin(Δφ / 2) +
        Math.cos(φ1) * Math.cos(φ2) *
        Math.sin(Δλ / 2) * Math.sin(Δλ / 2);

    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    const d = R * c; // Distance in meters
    return d;
}

export function sortByDistance(items, lat, lon) {
    items.sort((a, b) => {
        const distanceToA = getDistance(lat, lon, a.geometry.coordinates[1], a.geometry.coordinates[0]);
        const distanceToB = getDistance(lat, lon, b.geometry.coordinates[1], b.geometry.coordinates[0]);
        return distanceToA - distanceToB;
    });
}