/** * SECTION 1: CONFIGURATION & GLOBAL STATE
 * Keep your "settings" at the top so they are easy to change 
 * when you switch from development to a real server.
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
 * This section handles getting data from the source (JSON or API) 
 * and performing the filtering math.
 */
async function getMatchesFromServer(filters, page) {
    if (CONFIG.MODE === 'DEV') {
        // Step A: Load and cache the JSON if it's the first run
        if (cachedMatches.length === 0) {
            const response = await fetch(CONFIG.LOCAL_PATH);
            const data = await response.json();
            cachedMatches = data.matches;
            populateFilters(cachedMatches);
        }

        // Step B: Apply filters to the cached data
        let filtered = cachedMatches.filter(m => {
            const matchSearch = !filters.query || m.name.toLowerCase().includes(filters.query.toLowerCase());
            // "all" or empty string acts as a wildcard (show everything)
            const matchSeason = !filters.season || filters.season === 'all' || m.season === filters.season;
            const matchYear = !filters.year || filters.year === 'all' || m.date.includes(filters.year);
            const matchTourney = !filters.tournament || filters.tournament === 'all' || m.tournament === filters.tournament;
            
            return matchSearch && matchSeason && matchYear && matchTourney;
        });

        // Step C: Handle Pagination (Splitting results into pages)
        const start = (page - 1) * CONFIG.PAGE_SIZE;
        const end = start + CONFIG.PAGE_SIZE;

        return {
            matches: filtered.slice(start, end),
            totalCount: filtered.length,
            hasMore: end < filtered.length
        };
    } else {
        // Step D: Production mode - fetch from live URL
        const params = new URLSearchParams({ ...filters, page, limit: CONFIG.PAGE_SIZE });
        const response = await fetch(`${CONFIG.API_URL}?${params}`);
        return await response.json();
    }
}

/**
 * SECTION 3: UI RENDERING
 * These functions are responsible for building HTML elements 
 * and putting them on the screen.
 */

// Generates the dropdown menus dynamically from the JSON data
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

// Helper to create a single dropdown's internal HTML
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

// Renders the match cards into the main container
function renderMatchUI(data, append = false) {
    const container = document.getElementById("matchList");
    const initialPrompt = document.getElementById("initialPrompt");

    if (initialPrompt) initialPrompt.classList.add('d-none');
    if (!append) container.innerHTML = "";

    document.getElementById("matchCount").innerText = `Matches Found: ${data.totalCount}`;

    // Show/Hide "No Results" message
    document.getElementById("noResults").classList.toggle('d-none', data.matches.length > 0 || append);

    data.matches.forEach(match => {
        const col = document.createElement("div");
        col.className = "col";
        col.innerHTML = `
            <a href="match_details.html?id=${match.id}" class="match-card h-100 text-decoration-none d-block p-4 bg-white rounded-4 shadow-sm border transition-all">
                <div class="d-flex justify-content-between align-items-start mb-2">
                    <span class="badge bg-secondary-subtle text-secondary border-0 small">${match.season}</span>
                    <span class="text-muted small fw-bold" style="font-size: 0.75rem;">${match.tournament}</span>
                </div>
                <h3 class="h5 fw-bold text-dark mb-1">${match.name}</h3>
                <p class="small text-muted mb-3"><i class="bi bi-calendar3 me-2"></i>${match.date}</p>
                <div class="score-display p-2 rounded-3 mb-3 text-center border bg-light">
                    <span class="fw-bold text-primary">${match.score}</span>
                </div>
                <div class="d-flex justify-content-between align-items-center mt-auto pt-2">
                    <span class="badge ${match.winner === 'Draw' ? 'bg-warning text-dark' : 'bg-primary-subtle text-primary'}">
                        ${match.winner === 'Draw' ? 'Draw' : 'Winner: ' + match.winner}
                    </span>
                    <span class="text-primary fw-bold small">Details <i class="bi bi-arrow-right"></i></span>
                </div>
            </a>`;
        container.appendChild(col);
    });

    // Show/Hide "Load More" button based on whether there's more data
    const loadMoreBtn = document.getElementById("loadMoreBtn");
    if (loadMoreBtn) loadMoreBtn.classList.toggle('d-none', !data.hasMore);
}

/**
 * SECTION 4: CONTROLLERS & EVENT LISTENERS
 * This section connects user interaction (clicks/typing) to the logic.
 */

// Orchestrates the loading and rendering process
async function updateView(isNewSearch = true) {
    const query = document.getElementById("searchInput").value;
    const season = document.getElementById("filterSeason").value;
    const year = document.getElementById("filterYear").value;
    const tournament = document.getElementById("filterTournament").value;

    // Check: Do we show the "Welcome" screen or load data?
    const hasInteracted = query.length > 0 || (season !== "" && season !== "all") || (year !== "" && year !== "all") || (tournament !== "" && tournament !== "all");

    if (isInitialLoad && !hasInteracted) {
        document.getElementById("initialPrompt").classList.remove('d-none');
        document.getElementById("matchCount").innerText = "Ready to search";
        
        // Background load just to fill up filters
        if(cachedMatches.length === 0) await getMatchesFromServer({query: ''}, 1);
        return;
    }

    isInitialLoad = false; 
    if (isNewSearch) currentPage = 1;

    document.getElementById("loadingSpinner").classList.remove('d-none');

    try {
        const data = await getMatchesFromServer({ query, season, year, tournament }, currentPage);
        renderMatchUI(data, !isNewSearch);
    } catch (e) {
        console.error("Data load failed", e);
    }

    document.getElementById("loadingSpinner").classList.add('d-none');
}

// ATTACH LISTENERS
document.getElementById("searchInput").addEventListener("input", () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => updateView(true), 500);
});

["filterSeason", "filterYear", "filterTournament"].forEach(id => {
    document.getElementById(id).addEventListener("change", () => updateView(true));
});

document.getElementById("loadMoreBtn")?.addEventListener("click", () => {
    currentPage++;
    updateView(false);
});

document.getElementById("resetFilters").addEventListener("click", () => {
    document.getElementById("searchInput").value = "";
    document.getElementById("filterSeason").selectedIndex = 0;
    document.getElementById("filterYear").selectedIndex = 0;
    document.getElementById("filterTournament").selectedIndex = 0;
    isInitialLoad = true;
    document.getElementById("matchList").innerHTML = "";
    document.getElementById("initialPrompt").classList.remove('d-none');
    updateView(true);
});

// Initialization
window.onload = () => updateView(true);
