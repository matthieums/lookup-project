/**
 * Applies a fade-out and shrink animation to a list of elements. 
 * The function dynamically calculates each element's height, 
 * sets it as a CSS variable for smooth animation, triggers the
 * animation, and removes the element from the DOM after the animation completes.
 * @param {Array} elements 
 */
export function fadeAndSlideOut(elements) {
    elements.forEach(element => {
        const elementHeight = element.offsetHeight + 'px';
        element.style.setProperty('--element-height', elementHeight);
        element.style.animationPlayState = 'running';
        element.addEventListener('animationend', () => {
            element.remove();
        })
    })
}
