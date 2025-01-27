import { CONFIG } from './config.js';
import { fadeAndSlideOut } from './animations.js';

export function hideUnnecessaryContainers(path) {
    let containersToHide = [];
    
    if (path === CONFIG.paths.indexView) {
        const submitCourseContainer = document.querySelector('.submit-course-container');
        const titlesContainer = document.querySelector('.titles-container')
        containersToHide.push(submitCourseContainer,titlesContainer);
    } else if (path === CONFIG.paths.teachersView) {
        const teacherContainer = document.querySelector('.teacher-container')
        containersToHide.push(teacherContainer)
    }
    fadeAndSlideOut(containersToHide);
}

export function formatResultsAsStrings(data) {
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


export function formatResultsAsCards(data) {
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

export function formatResultsAsTable(data) {
    // TO-DO: Make more reusable. This function is only usable on one type of data. 
    const tableBody = document.querySelector('.table-body')
    tableBody.innerHTML = ''

    data.forEach(({ id, name, students, place, schedule }) => {
        const row = document.createElement('tr');
        let studentCount = students.length;
        [name, students, place, schedule].forEach((value) => {
            const cell = document.createElement('td');
            if (value === students) {
                value = studentCount;
            }
            cell.textContent = value;
            row.appendChild(cell);
            row.id = id
        })
        tableBody.appendChild(row);
        row.classList.add('course-row')
        row.addEventListener('click', () => {
            window.location.href = `course/${id}`;
        })

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

/**
 * Shows or hides the loading indicator.
 * @param {Element} container - The container where the data is displayed.
 * @param {boolean} isLoading - Whether to show the loading symbol (true) or the data (false).
 */
    export function displayLoadingSpinner(isLoading, container) {
        const spinner = document.getElementById('spinner');
        if (isLoading) {
            // container fade out

            displaySpinner(container, spinner);
        } else {
            // container fade in

            hideSpinner(container, spinner);
        }
    }

    function displaySpinner(container, spinner) {
        container.classList.add('d-none');
        spinner.classList.remove('d-none');
    }

    function hideSpinner(container,spinner) {
        spinner.classList.add('d-none');        
        container.classList.remove('d-none');
    }