document.addEventListener('DOMContentLoaded', () => {
    let filteredData1 = data1;
    let filteredData2 = data2;
    const ctx1 = document.getElementById('companyChart1').getContext('2d');
    const ctx2 = document.getElementById('companyChart2').getContext('2d');

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

    function createChart(ctx, data, dataType) {
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
                            text: 'Date',
                            color: '#FFFFFF', // White color for the x-axis title
                            font: {
                                size: 22 // Adjust font size if needed
                            }
                        },
                        ticks: {
                            color: '#FFFFFF', // White color for the x-axis ticks
                            font: {
                                size: 20 // Adjust font size if needed
                            }
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: `${dataType} Value`,
                            color: '#FFFFFF', // White color for the y-axis title
                            font: {
                                size: 22 // Adjust font size if needed
                            }
                        },
                        ticks: {
                            color: '#FFFFFF', // White color for the y-axis ticks
                            font: {
                                size: 20 // Adjust font size if needed
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            color: '#FFFFFF', // White color for the legend labels
                            font: {
                                size: 25 // Adjust font size if needed
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
                        },
                        titleColor: '#FFFFFF', // White color for the tooltip title
                        bodyColor: '#FFFFFF' // White color for the tooltip body
                    }
                }
            }
        });
    }
    

    let chart1 = createChart(ctx1, filteredData1, 'Close');
    let chart2 = createChart(ctx2, filteredData2, 'Close');

    function updateCharts() {
        const selectedType = document.getElementById('dataType').value;
        const range = document.getElementById('timeRange').value;

        filteredData1 = filterDataByRange(data1, range);
        filteredData2 = filterDataByRange(data2, range);

        let newDataset1;
        switch (selectedType) {
            case 'Close':
                newDataset1 = filteredData1.closes;
                chart1.options.scales.y.title.text = 'Close Value';
                break;
            case 'Open':
                newDataset1 = filteredData1.opens;
                chart1.options.scales.y.title.text = 'Open Value';
                break;
            case 'High':
                newDataset1 = filteredData1.highs;
                chart1.options.scales.y.title.text = 'High Value';
                break;
            case 'Low':
                newDataset1 = filteredData1.lows;
                chart1.options.scales.y.title.text = 'Low Value';
                break;
        }
        const values1 = newDataset1;
        const lineColor1 = values1[values1.length - 1] > values1[0] ? 'rgba(0, 128, 0, 1)' : 'rgba(255, 0, 0, 1)';
        chart1.data.datasets[0].borderColor = lineColor1;
        chart1.data.datasets[0].data = newDataset1;
        chart1.data.labels = filteredData1.dates;
        chart1.data.datasets[0].label = `${selectedType} Value`;
        chart1.update();

        let newDataset2;
        switch (selectedType) {
            case 'Close':
                newDataset2 = filteredData2.closes;
                chart2.options.scales.y.title.text = 'Close Value';
                break;
            case 'Open':
                newDataset2 = filteredData2.opens;
                chart2.options.scales.y.title.text = 'Open Value';
                break;
            case 'High':
                newDataset2 = filteredData2.highs;
                chart2.options.scales.y.title.text = 'High Value';
                break;
            case 'Low':
                newDataset2 = filteredData2.lows;
                chart2.options.scales.y.title.text = 'Low Value';
                break;
        }
        const values2 = newDataset2;
        const lineColor2 = values2[values2.length - 1] > values2[0] ? 'rgba(0, 128, 0, 1)' : 'rgba(255, 0, 0, 1)';
        chart2.data.datasets[0].borderColor = lineColor2;
        chart2.data.datasets[0].data = newDataset2;
        chart2.data.labels = filteredData2.dates;
        chart2.data.datasets[0].label = `${selectedType} Value`;
        chart2.update();
    }

    document.getElementById('dataType').value = "Close";
    document.getElementById('timeRange').value = "5y";
    updateCharts();
    document.getElementById('dataType').addEventListener('change', updateCharts);
    document.getElementById('timeRange').addEventListener('change', updateCharts);
});