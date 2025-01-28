import { formatResultsAsCards, formatResultsAsStrings, formatResultsAsTable } from './domUtils.js';
import { getCookie } from './csrfUtils.js'
import { CONFIG } from './config.js';
import { displayLoadingSpinner, fadeAndSlideIn } from './animations.js';
    // TO-DO
    // Refactor the fetchanddisplaynearbyschool function and merge it with the 
    // fetchAndRender function
    // Answer my own question: Why did I use Post instead of Get for some fetch requests?

/**
 * Fetches data from the provided URL and renders the results.
 * @param {string} url - The URL to fetch data from.
 * @param {string} path - The path where the results will be rendered.
 */
export async function fetchAndRender(url, path) {
    const resultsContainer = document.querySelector('.results-container')
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
        displayLoadingSpinner(false, resultsContainer)
    }
}

// Renders data and adds a search bar
function renderResults(data, path) {
    if (data.length == 0) {
        const resultsContainer = document.querySelector('.results-container')
        resultsContainer.innerHTML = 'No results found'
    } else {
        if (path === CONFIG.paths.indexView) {
            formatResultsAsCards(data)
        } else if (path === CONFIG.paths.myCoursesView) {
            formatResultsAsTable(data)
        } else if (path === CONFIG.paths.teachersView) {
            formatResultsAsStrings(data)
        } else if (path === CONFIG.paths.schoolsView) {
            formatResultsAsStrings(data)
        }
    }
}

export async function fetchAndDisplayNearbySchools(params) {
    const resultsContainer = document.querySelector('.results-container');
    const featuredContainer = document.querySelector('.featured-container')
    displayLoadingSpinner(true, featuredContainer);

    try {
        const response = await fetch('/geoschool', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') },
            body: JSON.stringify({ 
                user_lat: params.user_lat,
                user_lon: params.user_lon,
                radius: params.radius
            })
        })

        if (!response.ok) {
            throw new Error('NETWORK RESPONSE WAS NOT OK');
        }
        const data = await response.json();
        if (data.error) {
            resultsContainer.innerHTML = `${data.error}`;
        } else {
            resultsContainer.innerHTML = '';
            let content = '';
            data.forEach(school => {
                content += `<div>${school.name}</div>`;
            });
            resultsContainer.innerHTML = content;
            fadeAndSlideIn(resultsContainer);
        }
    } catch (error) {
        console.error('Error:', error);
        resultsContainer.innerHTML = 'AN ERROR HAS OCCURRED';
    }
    displayLoadingSpinner(false, featuredContainer)
}
