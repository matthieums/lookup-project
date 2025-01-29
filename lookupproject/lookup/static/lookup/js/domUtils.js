import { CONFIG } from './config.js';
import { fadeAndSlideOut } from './animations.js';

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
        const header = object.name;
        const title = object.teacher;
        const text = object.description;
        const footer = object.target_audience;
        const imageUrl = object.illustration;

        const card = courseCardFactory(header, title, text, footer,  imageUrl);

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

// Allows for the creation of cards with appropriate data.
// I add the result class so it can be manipulated dynamically
function courseCardFactory(header, title, text, footer, imageUrl) {
    const card = document.createElement('div');
    card.classList.add('card', 'text-center', 'm-2', 'result', 'shadow-sm', 'card-clickable');

    const cardHeader = document.createElement('div');
    cardHeader.classList.add('card-header');
    cardHeader.textContent = header;

    const cardBody = document.createElement('div');
    cardBody.classList.add('card-body');

    const cardTitle = document.createElement('h5');
    cardTitle.classList.add('card-title');
    cardTitle.textContent = title;

    const cardText = document.createElement('p');
    cardText.classList.add('card-text');
    cardText.textContent = text;

    const cardFooter = document.createElement('div');
    cardFooter.classList.add('card-footer', 'text-body-secondary');
    cardFooter.textContent = footer;

    const img = document.createElement('img');
    img.classList.add('img-fluid', 'rounded-start');
    img.src = imageUrl;
    img.alt = title;

    card.appendChild(img);
    card.appendChild(cardBody);
    cardBody.append(cardTitle, cardText);
    card.appendChild(cardFooter);

    return card;

}