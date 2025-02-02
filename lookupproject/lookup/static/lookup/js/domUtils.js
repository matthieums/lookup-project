import { CONFIG } from './config.js';
import { fadeAndSlideOut } from './animations.js';
import { courseCardFactory } from './elementFactories.js';

export function hideUnnecessaryContainers(path) {
    let containersToHide = [];
    
    if (path === CONFIG.paths.indexView) {
        const titlesContainer = document.querySelector('.titles-container');
        const featuredContainer = document.querySelector('.featured-container');
        containersToHide.push(titlesContainer, featuredContainer);
    } else if (path === CONFIG.paths.teachersView) {
        const teacherContainer = document.querySelector('.teacher-container');
        containersToHide.push(teacherContainer);
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

    const cardGroup = document.createElement('div');
    cardGroup.classList.add('card-group');

    data.forEach((object) => {
        const id = object.id;
        const header = object.name;
        const title = object.teacher;
        const text = object.description;
        const footer = object.target_audience;
        const imageUrl = object.illustration;

        const card = courseCardFactory(id, header, title, text, footer,  imageUrl);

        card.addEventListener('click', (event) => {
            window.location.href = `${CONFIG.paths.course}/${event.currentTarget.id}`;
        })

        const cardCol = document.createElement('div');
        cardCol.classList.add('col-md-4');
        cardCol.appendChild(card);

        cardGroup.appendChild(cardCol);
    })
    resultsContainer.appendChild(cardGroup);
}

export function formatResultsAsTable(data) {
    // TO-DO: Make more reusable. This function is only usable on one type of data. 
    const tableBody = document.querySelector('.table-body')
    const table = document.querySelector('.table')
    tableBody.innerHTML = ''

    const totalCourses = document.querySelector('.courses-total')
    totalCourses.innerHTML = `Total: ${data.length} courses`

    data.forEach(({ id, name, students, place, schedule, capacity }) => {
        const row = document.createElement('tr');
        let studentCount = `${students.length} / ${capacity}`;
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
        table.classList.remove('d-none')
    })
}

// TO-DO: Add a function to format results as carrousel
// TO-DO: Add a function that fetches the appropriate data.
// => Refactor some parts of the view to send the required with
// appropriate filters: by most-recently added, and 1 per discipline for example?