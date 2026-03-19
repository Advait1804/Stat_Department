// points-table.js
let leagueData = {};

/**
 * Initialize page components and fetch data
 */
async function initialize() {
    // 1. Fetch and Load Navbar
    try {
        const navResponse = await fetch("cmn_navbar.html");
        if (navResponse.ok) {
            document.getElementById("navbar").innerHTML = await navResponse.text();
        }
    } catch (err) {
        console.error("Navbar failed to load:", err);
    }

    // 2. Fetch Points Table Data
    try {
        const response = await fetch("http://127.0.0.1:5000/point-table");
        leagueData = await response.json();

        setupSeasonSelector(leagueData.seasons);
        renderTable(leagueData.seasons[0]); // Load newest season by default
    } catch (err) {
        console.error("Error loading JSON data:", err);
    }
}

/**
 * Fills the dropdown with season options
 */
function setupSeasonSelector(seasons) {
    const selector = document.getElementById("seasonSelect");
    
    selector.innerHTML = seasons.map(s => 
        `<option value="${s}">Season ${s}</option>`
    ).join('');

    selector.addEventListener('change', (event) => {
        renderTable(event.target.value);
    });
}

/**
 * Generates the table HTML based on selected season
 */
function renderTable(season) {
    const tableBody = document.getElementById("pointsTableBody");
    const data = leagueData.tables[season] || [];

    if (data.length === 0) {
        tableBody.innerHTML = `<tr><td colspan="8" class="text-center py-5">No data available for this season.</td></tr>`;
        return;
    }

    tableBody.innerHTML = data.map(team => `
        <tr onclick="window.location.href='playerstep1.html?team=${encodeURIComponent(team.name)}'" class="clickable-row" style="cursor:pointer;">
            <td class="text-center"><span class="pos-badge">${team.pos}</span></td>
            <td>
                <div class="d-flex align-items-center">
                    <div class="team-logo-placeholder me-3">
                        <i class="bi bi-shield-fill text-primary"></i>
                    </div>
                    <span class="fw-bold text-dark">${team.name}</span>
                </div>
            </td>
            <td class="text-center fw-semibold text-secondary">${team.played}</td>
            <td class="text-center text-success fw-bold">${team.win}</td>
            <td class="text-center text-danger fw-bold">${team.loss}</td>
            <td class="text-center text-muted">${team.nr}</td>
            <td class="text-center"><span class="pts-badge">${team.pts}</span></td>
            <td class="text-center">
                <div class="form-container">
                    ${team.form.map(res => {
                        const statusClass = res === 'W' ? 'form-w' : (res === 'L' ? 'form-l' : 'form-d');
                        return `<span class="form-circle ${statusClass}">${res}</span>`;
                    }).join('')}
                </div>
            </td>
        </tr>
    `).join('');
}

// Start the app
document.addEventListener('DOMContentLoaded', initialize);
