
// Globals
var path = window.location.pathname;
const indexView = '/'
const teachersView = '/teachers'
const newSchoolView ='/newschool'
const schoolsView = '/schools'
const contactView = '/contact'
// If I change the API key, make sure I change it in the validators.py file too
const ApiKey = '931a2f65384241b19147a6b601733f10'


document.addEventListener('DOMContentLoaded', function () {

    if (path === indexView) {

        // Manage buttons to display appropriate results on index page 
        const categories = Array.from(document.querySelectorAll('.category'))

        categories.forEach(category => {
            const categoryName = category.textContent
            const fetchUrl = `courses/get/${categoryName}`
            category.addEventListener('click', (event) => {
                event.preventDefault();
                fetchAndRender(fetchUrl)
            })
        })

    } else if (path === newSchoolView) {
        const autoCompleteContainer = document.getElementById("autocomplete");
        const locationInput = document.getElementById("id_location");
        
        const autoCompleteInput = new autocomplete.GeocoderAutocomplete(
            autoCompleteContainer, 
            ApiKey, 
            { /* Geocoder options */ });

            autoCompleteInput.on('select', (location) => {
                if (location.properties) {
                    const address = location.properties.formatted;
                    console.log(address)
                    locationInput.value = address;
                }
            });
        
            autoCompleteInput.on('input', (text) => {
                locationInput.value = text;
            });



    } else if (path === teachersView) {
        const fetchUrl = ('/teachers/get')
        fetchAndRender(fetchUrl)
        
    } else if (path === schoolsView) {
        const fetchUrl = ('schools/get')
        fetchAndRender(fetchUrl)
    } 


    // Fetch data and call function to display data
    function fetchAndRender(url) {
        fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error')
            }
            return response.json();
        })
        .then(data => renderResults(data))
        .catch(error => {
            console.log('error', error)
        })
    }

    // Renders data and adds a search bar
    function renderResults(data) {
        let containersToHide = [];
        
        if (path === indexView) {
            const submitCourseContainer = document.querySelector('.submit-course-container');
            const categoriesContainer = document.querySelector('.categories-container');    
            containersToHide.push(categoriesContainer, submitCourseContainer);
        } else if (path === teachersView) {
            const teacherContainer = document.querySelector('.teacher-container')
            containersToHide.push(teacherContainer)
        }

        hideUnnecessaryContainers(containersToHide)

        if (path === indexView) {
            formatResultsAsCards(data)
        } else if (path === teachersView) {
            formatResultsAsStrings(data)
        } else if (path === schoolsView) {
            formatResultsAsStrings(data)
        }
        
        const resultsContainer = document.querySelector('.results-container')
        const searchBar = searchBarFactory()
        resultsContainer.prepend(searchBar);
    }

    function formatResultsAsStrings(data) {
        const resultsContainer = document.querySelector('.results-container');
        resultsContainer.innerHTML = '';
        
        data.forEach((object) => {
            const container = document.createElement('div');
            container.classList.add('result')
            const header = object.name;
            container.append(header)
            resultsContainer.append(container)
        })
    }

    function formatResultsAsCards(data) {
        const resultsContainer = document.querySelector('.results-container');
        resultsContainer.innerHTML = '';

        data.forEach((object) => {
            const card = document.createElement('div');
    
            const header = object.name;
            const title = object.teacher;
            const text = object.description;
            const footer = object.target_audience;

            const cardBody = courseCardFactory(header, title, text, footer);
            card.appendChild(cardBody);
            resultsContainer.append(cardBody);
        })
    }

    function hideUnnecessaryContainers(containers) {
        containers.forEach(container => {
            container.classList.add('d-none')
        })
    }


    function searchBarFactory() {
        const searchBar = document.createElement('input');
        searchBar.type = 'text'
        searchBar.placeholder = 'Search here'
        searchBar.classList.add('search-bar')

        searchBar.addEventListener('keyup', function(event) {
            searchQuery = event.target.value
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

    // Allows for the creation of cards with appropriate data.
    // I add the result class so it can be manipulated dynamically
    function courseCardFactory(header, title, text, footer) {
        const card = document.createElement('div');
        card.classList.add('card', 'text-center', 'm-4', 'result');

        const cardHeader = document.createElement('div');
        cardHeader.classList.add('card-header');
        cardHeader.textContent = header;

        const cardBody = document.createElement('div');
        cardBody.classList.add('card-body');

        const cardTitle = document.createElement('h5');
        cardTitle.classList.add('card-title');
        cardTitle.textContent = title;

        const cardText = document.createElement('card-text');
        cardText.classList.add('card-text');
        cardText.textContent = text;

        const cardFooter = document.createElement('div');
        cardFooter.classList.add('card-footer', 'text-body-secondary');
        cardFooter.textContent = footer

        card.append(cardHeader, cardBody, cardTitle, cardText, cardFooter);

        return card
    }

});