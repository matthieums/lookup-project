import { fetchAndRender } from "./fetchUtils.js";
/**
 * Sets up dynamic filters by adding event listeners to form select elements.
 * When a user selects a new option, the corresponding parameter in the `params` object is updated.
 * The function constructs a query string based on the selected filters and makes a request to fetch data.
 * Uses a debouncing technique to limit the number of fetch requests made when the user rapidly changes filters.
 * 
 * @param {Object} params - An object representing the filter parameters (e.g., discipline, age_group, radius, etc.).
 * The function will modify this object as the user interacts with the filter selections.
 */
export function setUpDynamicFilters(params, path) {
    const formSelects = Array.from(document.querySelectorAll('.form-select'));
    
    let timeout;

    formSelects.forEach((selectForm) => {
        selectForm.addEventListener('change', function (event) {
            const value = event.target.value;
            const selectType = selectForm.getAttribute('aria-label');
            params[selectType] = value ? value : null;
            
            clearTimeout(timeout);

            timeout = setTimeout(() => {
                const queryString = Object.entries(params)
                    .filter(([key, value]) => value !== null && value !== "")
                    .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
                    .join('&');

                const fetchUrl = `courses/get?${queryString}`;
                fetchAndRender(fetchUrl, path);
            }, 300);
        })
    })
}

export function searchBarFactory() {
    const searchBar = document.createElement('input');
    searchBar.type = 'text'
    searchBar.placeholder = 'Search here'
    searchBar.classList.add('search-bar')

    searchBar.addEventListener('keyup', function(event) {
        const searchQuery = event.target.value
            narrowResults(searchQuery)
    })
    return searchBar;
}


function narrowResults(searchQuery) {
    const allResults = document.querySelectorAll('.result')
    const normalizedQuery = searchQuery.toLowerCase()

    allResults.forEach(result => {
        let resultData;

        if (result.classList.contains('card')) {
            resultData = result.firstElementChild.textContent
        } else {           
            resultData = result.textContent
        }

        if (!resultData.toLowerCase().startsWith(normalizedQuery)) {
            result.classList.add('d-none')
        } else {
            result.classList.remove('d-none')
        }
    })
}
