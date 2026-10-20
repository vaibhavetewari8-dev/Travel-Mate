
document.addEventListener("DOMContentLoaded", function () {
    // 1. Initialize the map at Agra
    const map = L.map("map").setView([27.1767, 78.0081], 13);

    // 2. Load OpenStreetMap tiles
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap contributors"
    }).addTo(map);

    // 3. Connect the routing feature
    const routingControl = L.Routing.control({
        waypoints: [
            L.latLng(27.1751, 78.0421),
            L.latLng(27.1795, 78.0211)
        ],
        routeWhileDragging: false,
        showAlternatives: false
    }).addTo(map);

    // 4. Calculate distance and estimated fare
    routingControl.on("routesfound", function (event) {
        const route = event.routes[0];
        const distanceKm = route.summary.totalDistance / 1000;

        const baseFare = 30;
        const includedDistance = 1.5;
        const minRate = 14;
        const maxRate = 18;

        const extraDistance = Math.max(
            0,
            distanceKm - includedDistance
        );

        const fareMin = Math.round(
            baseFare + extraDistance * minRate
        );

        const fareMax = Math.round(
            baseFare + extraDistance * maxRate
        );

        const ceilingFare = Math.ceil(fareMax * 1.25);

        // 5. Update Shreya's HTML banner
        document.getElementById("distance-text").textContent =
            `Distance: ${distanceKm.toFixed(2)} km`;

        document.getElementById("fare-range").textContent =
            `Fair Range: ₹${fareMin} - ₹${fareMax}`;

        document.getElementById("max-cap").textContent =
            ceilingFare;

        document.getElementById("fare-banner").classList.remove("hidden");

        // 6. Send search data to Vaibhav's Flask API
        fetch("/api/save_search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                distance: Number(distanceKm.toFixed(2)),
                fare: fareMax
            })
        })
        .then(function (response) {
            if (!response.ok) {
                throw new Error("Failed to save search");
            }
            return response.json();
        })
        .then(function (data) {
            console.log("Backend response:", data);
        })
        .catch(function (error) {
            console.error("API error:", error);
        });
    });
});