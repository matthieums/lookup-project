import { searchBarFactory } from './filterAndSearchUtils.js';
import { displayLoadingSpinner, formatResultsAsCards, formatResultsAsStrings, formatResultsAsTable, hideUnnecessaryContainers } from './domUtils.js';
import { getCookie } from './csrfUtils.js'
import { CONFIG } from './config.js';

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
            displayLoadingSpinner(false, resultsContainer);
            throw new Error('Error fetching data');
        }
        const data = await response.json();
        renderResults(data, path); 
    } catch (error) {
        displayLoadingSpinner(false, resultsContainer);
        console.error('Error:', error);
    }
}

    // Renders data and adds a search bar
    function renderResults(data, path) {
        const resultsContainer = document.querySelector('.results-container')
        hideUnnecessaryContainers(path)

        if (path === CONFIG.paths.indexView) {
            formatResultsAsCards(data)
        } else if (path === CONFIG.paths.myCoursesView) {
            formatResultsAsTable(data)
        } else if (path === CONFIG.paths.teachersView) {
            formatResultsAsStrings(data)
        } else if (path === CONFIG.paths.schoolsView) {
            formatResultsAsStrings(data)
        }
        displayLoadingSpinner(false, resultsContainer);
    }

    export async function fetchAndDisplayNearbySchools(params) {
        const resultsContainer = document.querySelector('.results-container');
        displayLoadingSpinner(true, resultsContainer)       
        fetch('/geoschool', {
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
        .then(response => {
            if (!response.ok) {
                displayLoadingSpinner(false, resultsContainer)       
                throw new Error('NETWORK RESPONSE WAS NOT OK')
            }
            return response.json();
        })
        .then(data => {
            displayLoadingSpinner(false, resultsContainer)       
            if (data.error) {
                resultsContainer.innerHTML = `${data.error}`;
            } else {
                resultsContainer.innerHTML = ''
                data.forEach(school => {
                    resultsContainer.innerHTML += school.name;
                });
            }
        })
        .catch(error => {
            displayLoadingSpinner(false, resultsContainer)       
            console.error('Error:', error);
            document.querySelector('.nearby-schools-container').innerHTML = 'AN ERROR HAS OCCURED';
        });
    }
   
