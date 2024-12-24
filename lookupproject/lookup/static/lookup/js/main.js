// Globals
var path = window.location.pathname;
const indexView = '/'
const teachersView = '/teachers'
const newSchoolView ='/newschool'

document.addEventListener('DOMContentLoaded', function () {



    if (path === indexView) {

        // Manage buttons to display appropriate results on index page 
        const categories = Array.from(document.querySelectorAll('.category'))

        categories.forEach(category => {
            const categoryName = category.textContent
            const fetchUrl = `courses/get/${categoryName}`
            category.addEventListener('click', (event) => {
                event.preventDefault();
                fetchData(fetchUrl)
            })
        })


    } else if (path === newSchoolView) {
        const addressInput = document.getElementById('id_location');

        addressInput.addEventListener('keyup', function(event) {
            let addressToSearch = event.target.value;
            checkAddress(addressToSearch);
        })

    } else if (path === teachersView) {
        const fetchUrl = ('/teachers/get')
        fetchData(fetchUrl)
        
    }


    // Fetch data and call function to display data
    function fetchData(url) {
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

    

    // Geoapify's address checker
    // https://www.geoapify.com/address-autocomplete/
    function checkAddress(address) {
        const ApiKey = '931a2f65384241b19147a6b601733f10'
        const url = `https://api.geoapify.com/v1/geocode/search?text=${encodeURIComponent(address)}&apiKey=${ApiKey}`;

        fetch(url).then(response => response.json())
        .then(result => {
            if (result.features.length === 0) {
                console.log("The address is not found");
            } else {
                console.log("Matched address:")
                console.log(result.features[0]);
            }
        })
        .catch(error => console.log('error', error));
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