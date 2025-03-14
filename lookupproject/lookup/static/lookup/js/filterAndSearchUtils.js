import { fetchAndRender } from "./fetchUtils.js";
import { hideUnnecessaryContainers } from "./domUtils.js";
import { initializeUserCoordinates } from "./geoUtils.js"
import { displayLoadingSpinner, fadeAndSlideIn } from "./animations.js";
import { searchBarFactory } from './elementFactories.js';


/**
 * Initializes parameters for the filters.
 * @returns {Promise<Object>} Resolves to an object containing filter parameters.
 */
export async function initializeParams() {
    let params = {
        discipline: null,
        age_group: null,
        radius: null,
        user_lon: null,
        user_lat: null
    };
    
    const coordinates = await initializeUserCoordinates();
    params.user_lat = coordinates[0];
    params.user_lon = coordinates[1];
    params.radius = setDefaultRadius();

    return params
}


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
    const resultsContainer = document.querySelector('.results-container')
    let timeout;

    formSelects.forEach((selectForm) => {
        selectForm.addEventListener('change', (event) => {
            displayLoadingSpinner(true, resultsContainer)
            if (!document.querySelector('.search-bar')) {
                appendSearchBar();
                hideUnnecessaryContainers(path);
            }

            const value = event.target.value;
            const selectType = selectForm.getAttribute('aria-label');
            params[selectType] = value ? value : null;
            
            clearTimeout(timeout);

            timeout = setTimeout(() => {
                const queryString = queryStringBuilder(params)


                const fetchUrl = `courses/get?${queryString}`;
                fetchAndRender(fetchUrl, path);
            }, 300);
        })
    })
}


export function narrowResults(searchQuery) {
    const allResults = document.querySelectorAll('.result')
    const normalizedQuery = searchQuery.toLowerCase()
    const resultsCountContainer = document.getElementById('results-count');
    let count = parseInt(resultsCountContainer.innerHTML)

    allResults.forEach(result => {
        let resultData;

        if (result.classList.contains('card')) {
            resultData = result.querySelector('.card-title').textContent;
        } else {           
            resultData = result.textContent
        }

        if (!resultData.toLowerCase().startsWith(normalizedQuery)) {
            result.parentElement.classList.add('d-none');
            if (count > 0) {
                count = Array.from(allResults).filter(result => !result.parentElement.classList.contains('d-none')).length;;
            }
            resultsCountContainer.innerHTML = count;
        } else {
            result.parentElement.classList.remove('d-none');
            count = Array.from(allResults).filter(result => !result.parentElement.classList.contains('d-none')).length;;
            resultsCountContainer.innerHTML = count;
        }
    })
}


/**
 * Provides a default radius for filtering.
 * @returns {number} The default radius in meters.
 */
export function setDefaultRadius() {
    const defaultRadius = 1000
    return defaultRadius
}

function appendSearchBar() {
    const searchBarContainer = document.querySelector('.search-bar-container')
    const searchBar = searchBarFactory()
    searchBar.addEventListener('keyup', function(event) {
        const searchQuery = event.target.value
        narrowResults(searchQuery)
    })
    searchBarContainer.prepend(searchBar)
}


export function displayResultsCount(data) {
    const count = data.length;
    const noResults = 'No results found';
    const container = document.getElementById('results-count');

    if ( count > 0) {
        container.innerHTML = count;
    } else {
        container.innerHTML = noResults;
    }
    fadeAndSlideIn(container.parentElement)
}

export function queryStringBuilder(params) {
    return Object.entries(params)
    .filter(([key, value]) => value !== null && value !== "")
    .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
    .join('&');
}