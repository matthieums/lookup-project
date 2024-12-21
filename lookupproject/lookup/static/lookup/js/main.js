document.addEventListener('DOMContentLoaded', function () {
    var path = window.location.pathname;

    if (path === '/') {

        // Manage buttons to display appropriate results on index page 
        const categoriesContainer = document.querySelector('.categories-container')
        const resultsContainer = document.querySelector('.results-container')
        const categories = Array.from(document.querySelectorAll('.category'))

        categories.forEach(category => {
            category.addEventListener('click', (event) => {
                event.preventDefault();
                fetchCourseData(category.innerHTML, categoriesContainer, resultsContainer)
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


    // Fetch and display data
    function fetchCourseData(categoryName, categoriesContainer, resultsContainer) {
        fetch(`courses/get/${categoryName}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error')
            }
            return response.json();
        })
        .then(data => renderResults(data, categoriesContainer, resultsContainer))
        .catch(error => {
            console.log('error', error)
        })
    }

    // Render data from lists
    function renderResults(data, parentElement, childElement) {
        parentElement.classList.add('d-none');
        childElement.innerHTML = '';

        data.forEach((piece) => {
            const newElement = document.createElement('p')
            newElement.innerHTML = piece.name
            childElement.append(newElement)
        })
    }

});