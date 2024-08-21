document.addEventListener('DOMContentLoaded', () => {
    // Fetch login status from the server
    fetch('/db/admin')
        .then(response => response.json())
        .then(data => {
            if (!data.is_admin) {
                // Hide the statistics menu item if the user is not an admin
                window.location.href = '/login';
            }
        })
        .catch(error => {
            console.error('Error checking admin status:', error);
        });

    const startDateInput = document.getElementById('startDate');
    const endDateInput = document.getElementById('endDate');
    const applyFiltersButton = document.getElementById('applyFilters');
    
    // Store references to existing charts
    const charts = {
        loginInteractions: null,
        sharesInteractions: null,
        buyShare: null
    };

    let today = new Date();

    // Get tomorrow's date
    let tomorrow = new Date(today);
    tomorrow.setDate(today.getDate() + 1);  // Add one day

    // Set default values for the date inputs
    today = today.toISOString().split('T')[0];
    tomorrow = tomorrow.toISOString().split('T')[0];
    
    startDateInput.value = today;
    endDateInput.value = tomorrow;

    applyFiltersButton.addEventListener('click', () => {
        const startDate = startDateInput.value;
        const endDate = endDateInput.value;
        
        // Fetch data from API with the selected date range
        fetchStatistics(startDate, endDate);
    });

    function fetchStatistics(startDate, endDate) {
        fetch(`/db/login_interactions?startDate=${startDate}&endDate=${endDate}`)
            .then(response => response.json())
            .then(data => renderLoginInteractionsGraph(data));
        
        fetch(`/db/shares_interactions?startDate=${startDate}&endDate=${endDate}`)
            .then(response => response.json())
            .then(data => renderSharesInteractionsGraph(data));
        
        fetch(`/db/buy_interactions?startDate=${startDate}&endDate=${endDate}`)
            .then(response => response.json())
            .then(data => renderBuyShareGraph(data));
    }
    
    function renderGraph(elementId, data, chartOptions) {
        const ctx = document.getElementById(elementId).getContext('2d');
        
        // Destroy existing chart if it exists
        if (charts[elementId]) {
            charts[elementId].destroy();
        }
        
        // Create new chart
        charts[elementId] = new Chart(ctx, chartOptions);
    }

    function renderLoginInteractionsGraph(data) {
        const chartOptions = {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Number of Logins',
                    data: data.values,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'white',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Date',
                            color: 'white'
                        },
                        ticks: {
                            color: 'white'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Number of Logins',
                            color: 'white'
                        },
                        ticks: {
                            color: 'white'
                        },
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            color: 'white'
                        }
                    }
                }
            }
        };
        renderGraph('loginInteractionsGraph', data, chartOptions);
    }
    
    function renderSharesInteractionsGraph(data) {
        const chartOptions = {
            type: 'pie',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Shares Interactions',
                    data: data.values,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: 'white',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        labels: {
                            color: 'white'
                        }
                    }
                }
            }
        };
        renderGraph('sharesInteractionsGraph', data, chartOptions);
    }
    
    function renderBuyShareGraph(data) {
        const chartOptions = {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Amount Spent on Shares',
                    data: data.values,
                    borderColor: 'white',
                    backgroundColor: 'rgba(40, 167, 69, 0.2)',
                    borderWidth: 1,
                    pointBackgroundColor: 'white',
                    pointBorderColor: 'white'
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Date',
                            color: 'white'
                        },
                        ticks: {
                            color: 'white'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Amount Spent',
                            color: 'white'
                        },
                        ticks: {
                            color: 'white'
                        },
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            color: 'white'
                        }
                    }
                }
            }
        };
        renderGraph('buyShareGraph', data, chartOptions);
    }
    
    // Initial load with today's date
    fetchStatistics(today, tomorrow);
});
