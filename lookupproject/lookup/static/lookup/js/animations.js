/**
 * Applies a fade-out and shrink animation to a list of elements. 
 * The function dynamically calculates each element's height, 
 * sets it as a CSS variable for smooth animation, triggers the
 * animation, and removes the element from the DOM after the animation completes.
 * @param {Array|Element} elements
 */


/**
 * Shows or hides the loading indicator.
 * @param {Element} container - The container where the data is displayed.
 * @param {boolean} isLoading - Whether to show the loading symbol (true) or the data (false).
 */
export async function displayLoadingSpinner(isLoading, container) {
    if (isLoading) {
        displaySpinner(container);
    } else {
        hideSpinner(container);
    }
}

function displaySpinner(container) {
    const spinner = document.getElementById('spinner')
    container.classList.add('d-none')
    spinner.classList.remove('d-none')
}

function hideSpinner(container) {
    const spinner = document.getElementById('spinner')
    spinner.classList.add('d-none')
    fadeAndSlideIn(container)
}

export function fadeAndSlideOut(elements) {
    const elementsArray = Array.isArray(elements) ? elements : [elements];

    elementsArray.forEach(element => {
        element.style.animationName = 'fade-out';
        element.style.animationDuration = '0.5s';
        element.style.animationTimingFunction = 'ease';
        element.style.animationIterationCount = '1'; 
        element.style.animationPlayState = 'running';        
        element.addEventListener('animationend', () => {
            element.style.animationPlayState = 'paused';
            element.classList.add('d-none') ;
        }, { once: true });
    })
}


export function fadeAndSlideIn(elements) {
    const elementsArray = Array.isArray(elements) ? elements : [elements];

    elementsArray.forEach(element => {
        element.style.animationName = 'fade-in';
        element.style.animationDuration = '1s';
        element.style.animationTimingFunction = 'ease';
        element.style.animationIterationCount = '1'; 
        element.style.animationPlayState = 'running';
        element.classList.remove('d-none')
        element.addEventListener('animationend', () => {
            element.style.animationPlayState = 'paused'
        }, { once: true });
    })
}
