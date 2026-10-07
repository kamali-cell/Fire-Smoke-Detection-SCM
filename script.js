function loginUser() {
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    if (username === "admin" && password === "admin123") {
        alert("Login successful!");
        window.location.href = "/dashboard";
    } else {
        alert("Invalid username or password!");
    }
}

function detectFire() {
    fetch("/add-detection/fire")
        .then(response => response.text())
        .then(() => {
            document.getElementById("fireStatus").innerHTML = "FIRE!";
            document.getElementById("fireStatus").className = "number danger";
            document.getElementById("fireMessage").innerHTML = "🔥 Fire detected!";
            document.getElementById("alertCount").innerHTML = "1";
            document.getElementById("latestDetection").innerHTML =
                "🔥 FIRE DETECTED — Saved to database.";

            alert("⚠️ FIRE DETECTED!\n\nDetection saved to database.");

            loadDetectionHistory();
        })
        .catch(error => {
            console.error(error);
            alert("Error saving fire detection!");
        });
}

function detectSmoke() {
    fetch("/add-detection/smoke")
        .then(response => response.text())
        .then(() => {
            document.getElementById("smokeStatus").innerHTML = "SMOKE!";
            document.getElementById("smokeStatus").className = "number danger";
            document.getElementById("smokeMessage").innerHTML = "💨 Smoke detected!";
            document.getElementById("alertCount").innerHTML = "1";
            document.getElementById("latestDetection").innerHTML =
                "💨 SMOKE DETECTED — Saved to database.";

            alert("⚠️ SMOKE DETECTED!\n\nDetection saved to database.");

            loadDetectionHistory();
        })
        .catch(error => {
            console.error(error);
            alert("Error saving smoke detection!");
        });
}

function resetSystem() {
    document.getElementById("fireStatus").innerHTML = "SAFE";
    document.getElementById("fireStatus").className = "number safe";

    document.getElementById("smokeStatus").innerHTML = "SAFE";
    document.getElementById("smokeStatus").className = "number safe";

    document.getElementById("fireMessage").innerHTML = "No fire detected";
    document.getElementById("smokeMessage").innerHTML = "No smoke detected";

    document.getElementById("alertCount").innerHTML = "0";
    document.getElementById("latestDetection").innerHTML =
        "No detection recorded.";
}

function loadDetectionHistory() {
    fetch("/api/detections")
        .then(response => response.json())
        .then(data => {
            let tableBody = document.getElementById("detectionTableBody");

            if (!tableBody) {
                return;
            }

            tableBody.innerHTML = "";

            if (data.length === 0) {
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="4">No detections found.</td>
                    </tr>
                `;
                return;
            }

            data.forEach(record => {
                tableBody.innerHTML += `
                    <tr>
                        <td>${record.id}</td>
                        <td>${record.type.toUpperCase()}</td>
                        <td>${record.time}</td>
                        <td>${record.status}</td>
                    </tr>
                `;
            });
        })
        .catch(error => {
            console.error("Error loading detection history:", error);
        });
}

function loadChangeRequests() {
    fetch("/api/change-requests")
        .then(response => response.json())
        .then(data => {
            let tableBody = document.getElementById("changeRequestBody");

            if (!tableBody) {
                return;
            }

            tableBody.innerHTML = "";

            if (data.length === 0) {
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="6">No change requests found.</td>
                    </tr>
                `;
                return;
            }

            data.forEach(request => {
                tableBody.innerHTML += `
                    <tr>
                        <td>${request.id}</td>
                        <td>${request.title}</td>
                        <td>${request.description}</td>
                        <td>${request.priority}</td>
                        <td>${request.status}</td>
                        <td>${request.time}</td>
                    </tr>
                `;
            });
        })
        .catch(error => {
            console.error("Error loading change requests:", error);
        });
}

function loadConfigurationItems() {
    fetch("/api/configuration-items")
        .then(response => response.json())
        .then(data => {
            let tableBody = document.getElementById("configurationItemBody");

            if (!tableBody) {
                return;
            }

            tableBody.innerHTML = "";

            if (data.length === 0) {
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="6">No configuration items found.</td>
                    </tr>
                `;
                return;
            }

            data.forEach(item => {
                tableBody.innerHTML += `
                    <tr>
                        <td>${item.id}</td>
                        <td>${item.name}</td>
                        <td>${item.type}</td>
                        <td>${item.version}</td>
                        <td>${item.status}</td>
                        <td>${item.owner}</td>
                    </tr>
                `;
            });
        })
        .catch(error => {
            console.error("Error loading configuration items:", error);
        });
}

document.addEventListener("DOMContentLoaded", function () {
    loadDetectionHistory();
    loadChangeRequests();
    loadConfigurationItems();
});