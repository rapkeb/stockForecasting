document.addEventListener('DOMContentLoaded', () => {

const statisticsMenuItem = document.getElementById('statisticsMenuItem');

// Fetch login status from the server
fetch('/db/admin')
    .then(response => response.json())
    .then(data => {
        if (!data.is_admin) {
            // Hide the statistics menu item if the user is not an admin
            statisticsMenuItem.style.display = 'none';
        }
    })
    .catch(error => {
        console.error('Error checking admin status:', error);
    });

// Determine the current path
const currentPath = window.location.pathname;
// Define the paths where you want to redirect logged-in users
const authPages = ['/login', '/register'];
// Check if the current page is an authentication page
const isAuthPage = authPages.includes(currentPath);

// Fetch login status from the server
fetch('/db/auth')
    .then(response => response.json())
    .then(data => {
        if (data.is_logged_in) {
            if (isAuthPage) {
                // Redirect to the index page if already logged in and on an auth page
                window.location.href = '/index';  // Replace with your index page URL
            }
        } else {
            // Redirect to login page if not logged in and on an auth page
            if (!isAuthPage) {
                window.location.href = '/login';  // Replace with the login page URL
            }
        }
    })
    .catch(error => {
        console.error('Error checking login status:', error);
        // Optionally handle the error, e.g., show a message to the user
    });

});