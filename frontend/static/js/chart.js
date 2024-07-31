document.addEventListener('DOMContentLoaded', () => {
    let filtereddata = data;
    const ctx = document.getElementById('companyChart').getContext('2d');

    function filterDataByRange(data, range) {
        const endDate = moment();
        let startDate;
        switch (range) {
            case '5d':
                startDate = endDate.clone().subtract(5, 'days');
                break;
            case '1m':
                startDate = endDate.clone().subtract(1, 'month');
                break;
            case '1y':
                startDate = endDate.clone().subtract(1, 'year');
                break;
            case '5y':
                startDate = endDate.clone().subtract(5, 'years');
                break;
            default:
                startDate = endDate.clone().subtract(5, 'years');
        }

        return {
            dates: data.dates.filter(date => moment(date).isBetween(startDate, endDate)),
            opens: data.opens.filter((_, index) => moment(data.dates[index]).isBetween(startDate, endDate)),
            closes: data.closes.filter((_, index) => moment(data.dates[index]).isBetween(startDate, endDate)),
            highs: data.highs.filter((_, index) => moment(data.dates[index]).isBetween(startDate, endDate)),
            lows: data.lows.filter((_, index) => moment(data.dates[index]).isBetween(startDate, endDate))
        };
    }

    if (window.myChart) {
        window.myChart.destroy();
    }
    window.myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.dates,
            datasets: [{
                label: 'Close Value',
                data: data.closes,
                borderColor: 'rgba(255, 0, 0, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                fill: false
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'month'
                    },
                    title: {
                        display: true,
                        text: 'Date',
                        color: '#ffffff', // Title color for the x-axis
                        font: {
                            size: 22 // Adjust font size if needed
                        }
                    },
                    ticks: {
                        color: '#ffffff', // Color for the x-axis labels
                        font: {
                            size: 20 // Adjust font size if needed
                        }
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Close Value',
                        color: '#ffffff', // Title color for the y-axis
                        font: {
                            size: 22 // Adjust font size if needed
                        }
                    },
                    ticks: {
                        color: '#ffffff', // Color for the y-axis labels
                        font: {
                            size: 20 // Adjust font size if needed
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: '#ffffff', // Color for the legend labels
                        font: {
                            size: 25 // Adjust font size if needed
                        }
                    }
                },
                tooltip: {
                    titleColor: '#ffffff', // Color for tooltip titles
                    bodyColor: '#ffffff' // Color for tooltip body text
                }
            }
        }
    });
    
    const values = data['closes'];
    const lineColor = values[values.length - 1] > values[0] ? 'rgba(0, 128, 0, 1)' : 'rgba(255, 0, 0, 1)';
    myChart.data.datasets[0].borderColor = lineColor;
    myChart.update();
    updateAverageAnnualReturn();

    const createChart = (dataType) => {
        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.dates,
                datasets: [{
                    label: `${dataType} Value`,
                    data: data[dataType.toLowerCase()],
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    fill: false
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'month'
                        },
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: `${dataType} Value`
                        }
                    }
                }
            }
        });
    }

    document.getElementById('dataType').addEventListener('change', (event) => {
        const selectedType = event.target.value;
        let newDataset;
        const range = document.getElementById('timeRange').value;
        filtereddata = filterDataByRange(data, range);
        switch (selectedType) {
            case 'Close':
                newDataset = filtereddata.closes;
                myChart.options.scales.y.title.text = 'Close Value';
                break;
            case 'Open':
                newDataset = filtereddata.opens;
                myChart.options.scales.y.title.text = 'Open Value';
                break;
            case 'High':
                newDataset = filtereddata.highs;
                myChart.options.scales.y.title.text = 'High Value';
                break;
            case 'Low':
                newDataset = filtereddata.lows;
                myChart.options.scales.y.title.text = 'Low Value';
                break;
        }
        const values = newDataset
        const lineColor = values[values.length - 1] > values[0] ? 'rgba(0, 128, 0, 1)' : 'rgba(255, 0, 0, 1)';
        myChart.data.datasets[0].borderColor = lineColor;
        myChart.data.datasets[0].data = newDataset;
        myChart.data.datasets[0].label = `${selectedType} Value`;
        myChart.update();
        updateAverageAnnualReturn();
    });

    document.getElementById('timeRange').addEventListener('change', (event) => {
        const rangeType = event.target.value;
        filtereddata = filterDataByRange(data, rangeType);
        const selectedType = document.getElementById('dataType').value;
        switch (selectedType) {
            case 'Close':
                newDataset = filtereddata.closes;
                myChart.options.scales.y.title.text = 'Close Value';
                break;
            case 'Open':
                newDataset = filtereddata.opens;
                myChart.options.scales.y.title.text = 'Open Value';
                break;
            case 'High':
                newDataset = filtereddata.highs;
                myChart.options.scales.y.title.text = 'High Value';
                break;
            case 'Low':
                newDataset = filtereddata.lows;
                myChart.options.scales.y.title.text = 'Low Value';
                break;
        }
        
        const values = newDataset
        const lineColor = values[values.length - 1] > values[0] ? 'rgba(0, 128, 0, 1)' : 'rgba(255, 0, 0, 1)';
        myChart.data.datasets[0].borderColor = lineColor;
        myChart.data.datasets[0].data = newDataset;
        myChart.data.labels = filtereddata.dates;
        myChart.data.datasets[0].label = `${selectedType} Value`;
        myChart.update();
        updateAverageAnnualReturn();
    });

    // Fetch current share price
    async function fetchCurrentPrice() {
        const shareName = document.getElementById("share").innerText.trim();
        const response = await fetch(`/current-price?company=${shareName}`);
        const data = await response.json();
        document.getElementById('currentPrice').innerText = `$${data.price.toFixed(2)}`;
    }

    fetchCurrentPrice();

    document.getElementById('buyButton').addEventListener('click', async () => {
        const quantity = document.getElementById('shareQuantity').value;
        const currentPrice = parseFloat(document.getElementById('currentPrice').innerText.replace('$', ''));
        const response = await fetch('/buy-share', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                company: company,
                share: symbol,
                quantity: quantity,
                price: currentPrice
            })
        });
        if(response.ok)
        {
            alert("share added successfully");
        }
    });

    function calculateAverageAnnualReturn() {
        const closeValues = data.closes;
        const startValue = closeValues[0];
        const endValue = closeValues[closeValues.length - 1];
        const years = 5;
        const annualReturn = (((endValue / startValue)* 100)-100)/5;
        return annualReturn;
    }

    function updateAverageAnnualReturn() {
        const annualReturn = calculateAverageAnnualReturn();
        document.getElementById('rate').value = annualReturn.toFixed(2);
    }
    document.getElementById('predict_button').addEventListener('click', async() => {
        const resultElement = document.getElementById('result');
        const date = document.getElementById('selectedDate').value;
        const shareName = document.getElementById("share").innerText.trim();
        if (date) {
            const response = await fetch(`/predict?date=${encodeURIComponent(date)}&share=${encodeURIComponent(shareName)}`);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            // Example logic for showing prediction result
            // Replace with actual prediction logic
            resultElement.textContent = `${data.prediction}`;
            resultElement.style.display = 'block'; // Show the result
            window.scrollTo({
                top: document.body.scrollHeight,
                behavior: 'smooth'
            });
        } else {
            resultElement.textContent = 'Please select a date to get the prediction.';
            resultElement.style.display = 'block'; // Show the result
        }
    });

    // document.getElementById('predict_button').addEventListener('click', async () => {
    //     try {
    //         const date = document.getElementById("selectedDate").value;
    //         const shareName = document.getElementById("share").innerText.trim(); // Extract the share name
            
    //         // Fetch prediction with the selected date and share name
    //         const response = await fetch(`/predict?date=${encodeURIComponent(date)}&share=${encodeURIComponent(shareName)}`);
            
    //         // Check if the response is ok (status in the range 200-299)
    //         if (!response.ok) {
    //             throw new Error('Network response was not ok');
    //         }
    
    //         const data = await response.json();
    //         document.getElementById("result").innerHTML = data.prediction;
    //     } catch (error) {
    //         console.error('Error fetching prediction:', error);
    //         document.getElementById("result").innerHTML = 'Error fetching prediction';
    //     }
    // });

    document.getElementById('calculateButton').addEventListener('click', () => {
        const principal = parseFloat(document.getElementById('principal').value);
        const monthlyAddition = parseFloat(document.getElementById('monthlyAddition').value);
        const rate = parseFloat(document.getElementById('rate').value) / 100;
        const time = parseFloat(document.getElementById('time').value);

        let futureValue = principal;
        for (let i = 0; i < time * 12; i++) {
            futureValue = (futureValue + monthlyAddition) * (1 + rate / 12);
        }
        document.getElementById('futureValue').innerText = `$${futureValue.toFixed(2)}`;
    });

    const ctx1 = document.getElementById('recommendationChart').getContext('2d');
    let recommendationChart;

    async function fetchCurrentPrice() {
        const shareName = document.getElementById("share").innerText.trim();
        const response = await fetch(`/current-price?company=${shareName}`);
        const data = await response.json();
        document.getElementById('currentPrice').innerText = `$${data.price.toFixed(2)}`;
    }

    const fetchRecommendations = async () => {
        const url = `/recommendation?company=${symbol}`;
        try {
            const response = await fetch(url);
            const data = await response.json();
            
            if (data.length > 0) {
                const latestRecommendation = data[0];  // Assuming the latest is the first in the array
                
                // Prepare data for Chart.js
                const chartData = {
                    labels: ['Strong Buy', 'Buy', 'Hold', 'Sell', 'Strong Sell'],
                    datasets: [{
                        label: 'Analyst Recommendations',
                        data: [
                            latestRecommendation.strongBuy,
                            latestRecommendation.buy,
                            latestRecommendation.hold,
                            latestRecommendation.sell,
                            latestRecommendation.strongSell
                        ],
                        backgroundColor: [
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(255, 159, 64, 0.2)',
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(153, 102, 255, 0.2)',
                            'rgba(255, 206, 86, 0.2)'
                        ],
                        borderColor: [
                            'rgba(75, 192, 192, 1)',
                            'rgba(255, 159, 64, 1)',
                            'rgba(255, 99, 132, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 206, 86, 1)'
                        ],
                        borderWidth: 1
                    }]
                };

                // Initialize or update the chart
                if (recommendationChart) {
                    recommendationChart.destroy();
                }

                recommendationChart = new Chart(ctx1, {
                    type: 'pie',
                    data: chartData,
                    options: {
                        responsive: true, // Ensure the chart is responsive
                        maintainAspectRatio: false, // Allows the chart to fill its container
                        plugins: {
                            legend: {
                                position: 'top',
                                labels: {
                                    color: '#ffffff',
                                font: {
                                    size: 20,
                                }
                            }
                            },
                            tooltip: {
                                callbacks: {
                                    label: function(tooltipItem) {
                                        const label = tooltipItem.label;
                                        const value = tooltipItem.raw;
                                        return `${label}: ${value}`;
                                    }
                                }
                            }
                        }
                    }
                });
            } else {
                alert('No recommendations available.');
            }
        } catch (error) {
            console.error('Error fetching recommendations:', error);
        }
    };

    document.getElementById('fetchButton').addEventListener('click', fetchRecommendations);
});