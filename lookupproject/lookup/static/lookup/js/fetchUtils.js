import { formatResultsAsCards, formatResultsAsStrings, formatResultsAsTable } from './domUtils.js';
import { CONFIG } from './config.js';
import { displayLoadingSpinner } from './animations.js';
import { displayResultsCount } from './filterAndSearchUtils.js';

/**
 * Fetches data from the provided URL and renders the results.
 * @param {string} url - The URL to fetch data from.
 * @param {string} path - The path where the results will be rendered.
 */
export async function fetchAndRender(url, path) {
    const resultsContainer = document.querySelector('.results-container');

    displayLoadingSpinner(true, resultsContainer);
    
    try {
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error('Error fetching data');
        }
        const data = await response.json();
        renderResults(data, path);
    } catch (error) {
        console.error('Error:', error);
    } finally {
        displayLoadingSpinner(false, resultsContainer);
    }
}

// Renders data and adds a search bar
function renderResults(data, path) {
    if (path === CONFIG.paths.indexView) {
        displayResultsCount(data);
        formatResultsAsCards(data);
    } else if (path === CONFIG.paths.myCoursesView) {
        formatResultsAsTable(data);
    } else if (path === CONFIG.paths.teachersView) {
        formatResultsAsStrings(data);
    } else if (path === CONFIG.paths.schoolsView) {
        formatResultsAsStrings(data);
    }
}


export async function fetchAndDisplayClosestCityName(params) {
    const closestCityContainer = document.getElementById('closest-city')
    var requestOptions = {
        method: 'GET',
      };

    const lat = params.user_lat
    const lon = params.user_lon

    try {
        const response = await fetch(`https://api.geoapify.com/v1/geocode/reverse?lat=${lat}&lon=${lon}&apiKey=${CONFIG.apiKey}`, requestOptions)
        
        if (!response.ok) {
            console.error('Reverse Geogoder fetch returned an error')
        }

        const data = await response.json()
        const city = data.features[0]?.properties?.city;
        closestCityContainer.innerHTML = city

    } catch (error) {
        console.log(error)
        closestCityContainer.innerHTML = "Location not found"
    }
}