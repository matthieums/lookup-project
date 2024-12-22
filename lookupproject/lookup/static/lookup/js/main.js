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
            const newElement = document.createElement('p')
            newElement.innerHTML = course.name
            resultsContainer.append(newElement)
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
        return searchBar;
    }


});