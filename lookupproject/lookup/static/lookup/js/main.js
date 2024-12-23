document.addEventListener('DOMContentLoaded', function () {
    var path = window.location.pathname;

    if (path === '/') {

        // Manage buttons to display appropriate results on index page 
        const categories = Array.from(document.querySelectorAll('.category'))

        categories.forEach(category => {
            const categoryName = category.innerHTML
            category.addEventListener('click', (event) => {
                event.preventDefault();
                fetchCourseData(categoryName)
            })
        })


    } else if (path === '/newschool') {
        const addressInput = document.getElementById('id_location');
        addressInput.addEventListener('keyup', function(event) {
            let addressToSearch = event.target.value;
            checkAddress(addressToSearch);
        })

    } else if (path === '/teachers') {
        console.log('Welcome to the teachers page')

    } else if (path === '/courses') {
        console.log('Welcome to the courses page')
    
    } else if (path === '/schools') {
        console.log('Welcome to the schools page')
    } else if (path === '/newschool') {
        
    }


    // Fetch data and call function to display data
    function fetchCourseData(categoryName) {
        fetch(`courses/get/${categoryName}`)
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
        const submitCourseContainer = document.querySelector('.submit-course-container');
        const categoriesContainer = document.querySelector('.categories-container');
        const containersToHide = [categoriesContainer, submitCourseContainer];
        hideUnnecessaryContainers(containersToHide)

        const resultsContainer = document.querySelector('.results-container')
        resultsContainer.innerHTML = '';

        const searchBar = searchBarFactory()
        resultsContainer.appendChild(searchBar);

        data.forEach((course) => {
            const newParent = document.createElement('div')
            const newElement = document.createElement('a')
            newElement.href = `enroll/${course.id}`
            newElement.classList.add('result')
            newElement.textContent = course.name
            newParent.appendChild(newElement)
            resultsContainer.append(newParent)
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
        allResults.forEach(result => {
            const name = result.textContent
            if (!name.toLowerCase().startsWith(searchQuery.toLowerCase())) {
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

});