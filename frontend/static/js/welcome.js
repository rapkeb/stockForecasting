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

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('login-form');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        const username = form.querySelector('input[name="username"]').value;
        const password = form.querySelector('input[name="password"]').value;

        fetch('/db/login', { // Adjust URL to your backend service
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username: username, password: password }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Store user data in session storage or handle successful login
                sessionStorage.setItem('username', username);
                sessionStorage.setItem('user_id', data.user_id);
                window.location.href = `/front/homepage`;
            } else {
                // Show error message
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred during login. Please try again.');
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('register-form');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        const username = form.querySelector('input[name="username"]').value;
        const password = form.querySelector('input[name="password"]').value;
        const confirmPassword = form.querySelector('input[name="confirm_password"]').value;

        fetch('/db/register', { // Adjust URL to your backend service
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username: username, password: password, confirm_password: confirmPassword }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.href = '/front/login'; // Redirect to login page
            } else {
                // Show error message
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred during registration. Please try again.');
        });
    });
});


