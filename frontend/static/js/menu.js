document.addEventListener('DOMContentLoaded', () => {
    const hamburgerMenu = document.querySelector('.hamburger-menu');
    const sidebar = document.querySelector('.sidebar');
    
    hamburgerMenu.addEventListener('click', () => {
        sidebar.classList.toggle('active');
    });

    const logoutLink = document.getElementById('logoutLink');

    logoutLink.addEventListener('click', (event) => {
        event.preventDefault(); // Prevent the default link behavior
        
        // Make an API call to /db/logout
        fetch('/db/logout', {
            method: 'GET', // Use POST for logout
            headers: {
                'Content-Type': 'application/json'
            },
            // Optionally send any data needed for logout
            // body: JSON.stringify({ key: 'value' })
        })
        .then(response => {
            if (response.ok) {
                // Redirect to the homepage or login page after successful logout
                window.location.href = '/front/login';
            } else {
                // Handle error, e.g., show an error message
                console.error('Logout failed');
            }
        })
        .catch(error => {
            console.error('Error making logout request:', error);
        });
    });
});
