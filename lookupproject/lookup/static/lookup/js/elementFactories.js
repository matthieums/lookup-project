// Allows for the creation of cards with appropriate data.
// I add the result class so it can be manipulated dynamically
export function courseCardFactory(id, header, title, text, footer, imageUrl) {
    const card = document.createElement('div');
    card.classList.add('card', 'text-center', 'm-2', 'result', 'shadow-sm', 'card-clickable');
    card.id = id

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

/**
 * Creates a search bar html with filtering behaviour.
 * @returns {HTMLInputElement}
 */
export function searchBarFactory() {
    const searchBar = document.createElement('input');
    searchBar.type = 'text'
    searchBar.placeholder = 'Search here'
    searchBar.classList.add('search-bar')
    searchBar.classList.add('form-control')

    return searchBar;
}
