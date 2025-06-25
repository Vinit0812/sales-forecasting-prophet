const capDropdown = document.getElementById("capSelect");
const ctx = document.getElementById("forecastChart").getContext("2d");
let chartInstance = null;

async function loadCapIDs() {
    const response = await fetch("/api/cap_ids");
    const data = await response.json();
    data.cap_ids.forEach(id => {
        const option = document.createElement("option");
        option.value = id;
        option.textContent = id;
        capDropdown.appendChild(option);
    });
}

async function fetchForecast() {
    const capID = capDropdown.value;
    const response = await fetch(`/api/forecast/${capID}`);
    const data = await response.json();

    const labels = data.map(d => d.ds);
    const yhat = data.map(d => d.yhat);
    const yhatLower = data.map(d => d.yhat_lower);
    const yhatUpper = data.map(d => d.yhat_upper);

    if (chartInstance) {
        chartInstance.destroy();
    }

    chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: `Forecast (yhat) for ${capID}`,
                    data: yhat,
                    borderColor: 'blue',
                    fill: false,
                },
                {
                    label: 'Lower Bound (yhat_lower)',
                    data: yhatLower,
                    borderColor: 'lightblue',
                    borderDash: [5, 5],
                    fill: false,
                },
                {
                    label: 'Upper Bound (yhat_upper)',
                    data: yhatUpper,
                    borderColor: 'lightblue',
                    borderDash: [5, 5],
                    fill: false,
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom' },
                title: {
                    display: true,
                    text: `Forecast for ${capID}`
                }
            }
        }
    });
}

// Load Cap_IDs on page load
window.onload = loadCapIDs;
