/**
 * SECTION 1: CONFIGURATION & GLOBAL STATE
 */
const CONFIG = {
    MODE: 'PROD',
    LOCAL_PATH: 'match_wise.json',
    API_URL: 'http://127.0.0.1:5000/match-wise',
    PAGE_SIZE: 20
};

let currentPage = 1;
let debounceTimer;
let isInitialLoad = true;
let cachedMatches = [];


/**
 * SECTION 2: DATA & FILTER LOGIC
 */
async function getMatchesFromServer(filters, page) {

    if (CONFIG.MODE === 'DEV') {

        if (cachedMatches.length === 0) {
            const response = await fetch(CONFIG.LOCAL_PATH);
            const data = await response.json();
            cachedMatches = data.matches;
            populateFilters(cachedMatches);
        }

        let filtered = cachedMatches.filter(m => {
            const matchSearch = !filters.query || m.name.toLowerCase().includes(filters.query.toLowerCase());
            const matchSeason = !filters.season || filters.season === 'all' || m.season === filters.season;
            const matchYear = !filters.year || filters.year === 'all' || m.date.includes(filters.year);
            const matchTourney = !filters.tournament || filters.tournament === 'all' || m.tournament === filters.tournament;

            return matchSearch && matchSeason && matchYear && matchTourney;
        });

        const start = (page - 1) * CONFIG.PAGE_SIZE;
        const end = start + CONFIG.PAGE_SIZE;

        return {
            matches: filtered.slice(start, end),
            total: filtered.length,
            page: page,
            limit: CONFIG.PAGE_SIZE,
            hasMore: end < filtered.length
        };

    } else {

        const params = new URLSearchParams({
            ...filters,
            page: page,
            limit: CONFIG.PAGE_SIZE
        });

        const response = await fetch(`${CONFIG.API_URL}?${params}`);
        return await response.json();
    }
}


/**
 * SECTION 3: UI RENDERING
 */

function populateFilters(matches) {

    const seasons = new Set();
    const years = new Set();
    const tournaments = new Set();

    matches.forEach(m => {
        if (m.season) seasons.add(m.season);
        if (m.tournament) tournaments.add(m.tournament);

        const yearMatch = m.date.match(/\d{4}/);
        if (yearMatch) years.add(yearMatch[0]);
    });

    updateDropdown("filterSeason", seasons, "Season");
    updateDropdown("filterYear", Array.from(years).sort((a, b) => b - a), "Year");
    updateDropdown("filterTournament", tournaments, "Tournament");
}


function updateDropdown(id, values, label) {

    const select = document.getElementById(id);
    if (!select) return;

    let html = `<option value="" selected disabled>Select ${label}</option>`;
    html += `<option value="all">All ${label}s</option>`;

    values.forEach(val => {
        html += `<option value="${val}">${val}</option>`;
    });

    select.innerHTML = html;
}


/**
 * Render match cards
 */
function renderMatchUI(data) {

    const container = document.getElementById("matchList");
    const initialPrompt = document.getElementById("initialPrompt");

    if (initialPrompt) initialPrompt.classList.add('d-none');

    // IMPORTANT: clear previous results
    container.innerHTML = "";

    document.getElementById("matchCount").innerText =
        `Matches Found: ${data.total}`;

    document.getElementById("noResults")
        .classList.toggle('d-none', data.matches.length > 0);

    data.matches.forEach(match => {

        const col = document.createElement("div");
        col.className = "col";

        col.innerHTML = `
        <a href="match_details.html?id=${match.id}" 
           class="match-card h-100 text-decoration-none d-block p-4 bg-white rounded-4 shadow-sm border">

            <div class="d-flex justify-content-between mb-2">
                <span class="badge bg-secondary">${match.season}</span>
                <span class="small text-muted">${match.tournament}</span>
            </div>

            <h3 class="h5 fw-bold">${match.name}</h3>

            <p class="small text-muted">
                <i class="bi bi-calendar3 me-2"></i>${match.date}
            </p>

            <div class="p-2 text-center border bg-light mb-3">
                <span class="fw-bold text-primary">${match.score}</span>
            </div>

            <div class="d-flex justify-content-between">
                <span class="badge ${
                    match.winner === 'Draw'
                        ? 'bg-warning text-dark'
                        : 'bg-primary'
                }">
                    ${match.winner === 'Draw'
                        ? 'Draw'
                        : 'Winner: ' + match.winner}
                </span>

                <span class="text-primary fw-bold small">
                    Details →
                </span>
            </div>

        </a>`;

        container.appendChild(col);
    });
}


/**
 * Pagination UI
 */
function renderPagination(total, page, limit) {

    const container = document.getElementById("pagination");
    if (!container) return;

    container.innerHTML = "";

    const totalPages = Math.ceil(total / limit);

    for (let i = 1; i <= totalPages; i++) {

        const btn = document.createElement("button");

        btn.innerText = i;

        btn.className =
            (i === page)
                ? "btn btn-primary me-2"
                : "btn btn-outline-primary me-2";

        btn.addEventListener("click", () => {

            currentPage = i;

            // FIX: don't reset page
            updateView(false);

        });

        container.appendChild(btn);
    }
}


/**
 * SECTION 4: CONTROLLER
 */
async function updateView(isNewSearch = true) {

    const query = document.getElementById("searchInput").value;
    const season = document.getElementById("filterSeason").value;
    const year = document.getElementById("filterYear").value;
    const tournament = document.getElementById("filterTournament").value;

    if (isNewSearch) currentPage = 1;

    document.getElementById("loadingSpinner")
        .classList.remove('d-none');

    try {

        const data = await getMatchesFromServer(
            { query, season, year, tournament },
            currentPage
        );

        renderMatchUI(data);

        renderPagination(data.total, data.page, data.limit);

    } catch (e) {

        console.error("Data load failed", e);

    }

    document.getElementById("loadingSpinner")
        .classList.add('d-none');
}


/**
 * EVENT LISTENERS
 */

document.getElementById("searchInput")
.addEventListener("input", () => {

    clearTimeout(debounceTimer);

    debounceTimer =
        setTimeout(() => updateView(true), 500);

});


["filterSeason", "filterYear", "filterTournament"]
.forEach(id => {

    document.getElementById(id)
    .addEventListener("change", () => updateView(true));

});


document.getElementById("resetFilters")
.addEventListener("click", () => {

    document.getElementById("searchInput").value = "";

    document.getElementById("filterSeason").selectedIndex = 0;
    document.getElementById("filterYear").selectedIndex = 0;
    document.getElementById("filterTournament").selectedIndex = 0;

    currentPage = 1;

    updateView(true);

});


/**
 * Initialization
 */
window.onload = () => updateView(true);
