document.addEventListener('DOMContentLoaded', () => {
    const hamburgerMenu = document.querySelector('.hamburger-menu');
    const sidebar = document.querySelector('.sidebar');
    
    hamburgerMenu.addEventListener('click', () => {
        sidebar.classList.toggle('active');
    });
});
