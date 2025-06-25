let forecastChart = null;

function renderForecastChart(forecastData, capID) {
    const ctx = document.getElementById('forecastChart').getContext('2d');

    const labels = forecastData.map(item => item.ds);
    const yhat = forecastData.map(item => item.yhat);
    const yhatLower = forecastData.map(item => item.yhat_lower);
    const yhatUpper = forecastData.map(item => item.yhat_upper);

    if (forecastChart) {
        forecastChart.destroy();
    }

    forecastChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: `Forecast for ${capID}`,
                    data: yhat,
                    borderColor: 'blue',
                    borderWidth: 2,
                    fill: false,
                },
                {
                    label: 'Lower Bound',
                    data: yhatLower,
                    borderColor: 'lightblue',
                    borderDash: [5, 5],
                    fill: false,
                },
                {
                    label: 'Upper Bound',
                    data: yhatUpper,
                    borderColor: 'lightblue',
                    borderDash: [5, 5],
                    fill: false,
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: { display: true, text: 'Date' },
                    ticks: { autoSkip: true, maxTicksLimit: 15 }
                },
                y: {
                    title: { display: true, text: 'Sales Forecast' }
                }
            },
            plugins: {
                legend: { position: 'bottom' },
                title: {
                    display: true,
                    text: `Sales Forecast with Prophet for ${capID}`
                }
            }
        }
    });
}
