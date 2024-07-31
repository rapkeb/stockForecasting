let selectedCompanies = [];
let timer;

document.addEventListener('DOMContentLoaded', () => {
    populateSectorDropdown();
    getRandomCompanies();
});

function getRandomCompanies() {
    const companyDivs = document.querySelectorAll('.company-div');
    const companyArray = Array.from(companyDivs);
    const selectedCompanies = [];

    // Hide all companies initially
    companyDivs.forEach(div => div.style.display = 'none');

    // Randomly select 100 companies and make them visible
    while (selectedCompanies.length < 100 && companyArray.length > 0) {
        const randomIndex = Math.floor(Math.random() * companyArray.length);
        const selectedCompany = companyArray.splice(randomIndex, 1)[0];
        selectedCompanies.push(selectedCompany);
    }

    // Show only selected companies
    selectedCompanies.forEach(div => div.style.display = 'block');
}

function populateSectorDropdown() {
    const sectors = new Set();
    const companies = document.querySelectorAll('.company-div');
    companies.forEach(company => {
        sectors.add(company.dataset.sector);
    });
    
    const sectorFilter = document.getElementById('sector-filter');
    sectors.forEach(sector => {
        const option = document.createElement('option');
        option.value = sector;
        option.textContent = sector;
        sectorFilter.appendChild(option);
    });
}

function showChart(companyName, share) {
// Check if companyName is not in selectedCompanies
if (!selectedCompanies.includes(companyName)) {
// Redirect to the company page with the company name and sector as query parameters
window.location.href = `/company?company=${encodeURIComponent(companyName)}&share=${encodeURIComponent(share)}`;
}
}


function startSelectCompany(event, companyName) {
    event.preventDefault();
    timer = setTimeout(() => {
        toggleSelectCompany(companyName);
    }, 500);
}

function stopSelectCompany(event) {
    clearTimeout(timer);
}

function toggleSelectCompany(companyName) {
    const index = selectedCompanies.indexOf(companyName);
    if (index > -1) {
        selectedCompanies.splice(index, 1);
        document.querySelector(`[data-company="${companyName}"]`).classList.remove('selected');
    } else if (selectedCompanies.length < 2) {
        selectedCompanies.push(companyName);
        document.querySelector(`[data-company="${companyName}"]`).classList.add('selected');
    }
    document.getElementById('compare-button').style.display = selectedCompanies.length === 2 ? 'block' : 'none';
}

function compareCompanies() {
    if (selectedCompanies.length === 2) {
        window.location.href = `/compare?company1=${encodeURIComponent(selectedCompanies[0])}&company2=${encodeURIComponent(selectedCompanies[1])}`;
    }
}

function filterCompanies() {
    const searchInput = document.getElementById('search-input').value.toLowerCase();
    const sectorFilter = document.getElementById('sector-filter').value;
    const companies = document.querySelectorAll('.company-div');
    if(sectorFilter == '' && searchInput == '')
    {
        getRandomCompanies();
    }
    else
    {
        companies.forEach(company => {
            const companyName = company.dataset.company.toLowerCase();
            const companySector = company.dataset.sector;
            
            if ((companyName.includes(searchInput)) && 
                (sectorFilter === '' || companySector === sectorFilter)) {
                company.style.display = '';
            } else {
                company.style.display = 'none';
            }
        });
    }
}