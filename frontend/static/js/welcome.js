const ctx = document.getElementById('stockChart').getContext('2d');
let labels = Array.from({length: 100}, (_, i) => i);
let data = Array.from({length: 100}, () => Math.random() * 100);

const chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            label: 'Stock Price',
            data: data,
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderWidth: 1,
            fill: true,
        }]
    },
    options: {
        scales: {
            x: { display: false },
            y: { display: false, min: 0, max: 100 }
        },
        animation: {
            duration: 0
        },
        plugins: {
            legend: { display: false }
        }
    }
});

function updateChart() {
    data.push(Math.random() * 100);
    data.shift();
    chart.update();
}

setInterval(updateChart, 1000);
