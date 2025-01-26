import { searchBarFactory } from './filterAndSearchUtils.js';
import { formatResultsAsCards, formatResultsAsStrings, formatResultsAsTable, hideUnnecessaryContainers } from './domUtils.js';
import { getCookie } from './csrfUtils.js'
import { CONFIG } from './config.js';

    // TO-DO
    // Refactor the fetchanddisplaynearbyschool function and merge it with the 
    // fetchAndRender function
    // Answer my own question: Why did I use Post instead of Get for some fetch requests?

    // Fetch data and call function to display data
    export function fetchAndRender(url, path) {
        fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error')
            }
            return response.json();
        })
        .then(data => renderResults(data, path))
        .catch(error => {
            console.log('error', error)
        })
    }

    // Renders data and adds a search bar
    function renderResults(data, path) {
        const resultsContainer = document.querySelector('.results-container')

        hideUnnecessaryContainers(path)

        if (path === CONFIG.paths.indexView) {
            formatResultsAsCards(data)
            const searchBar = searchBarFactory()
            resultsContainer.prepend(searchBar);
        } else if (path === CONFIG.paths.myCoursesView) {
            formatResultsAsTable(data)
        } else if (path === CONFIG.paths.teachersView) {
            formatResultsAsStrings(data)
            const searchBar = searchBarFactory()
            resultsContainer.prepend(searchBar);
        } else if (path === CONFIG.paths.schoolsView) {
            formatResultsAsStrings(data)
            const searchBar = searchBarFactory()
            resultsContainer.prepend(searchBar);
        }
    }

    export async function fetchAndDisplayNearbyCourses(params) {
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
                throw new Error('NETWORK RESPONSE WAS NOT OK')
            }
            return response.json();
        })
        .then(data => {
            const nearbySchoolsContainer = document.querySelector('.nearby-schools-container');
            nearbySchoolsContainer.innerHTML = '';
    
            if (data.error) {
                nearbySchoolsContainer.innerHTML = `${data.error}`;
            } else {
                data.forEach(school => {
                    nearbySchoolsContainer.innerHTML += school.name;
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.querySelector('.nearby-schools-container').innerHTML = 'AN ERROR HAS OCCURED';
        });
    }
   
