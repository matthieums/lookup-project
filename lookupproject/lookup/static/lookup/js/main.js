import { initializeParams } from './geoUtils.js';
import { CONFIG } from './config.js';
import { fetchAndDisplayNearbyCourses } from './fetchUtils.js';
import { setUpDynamicFilters } from './filterAndSearchUtils.js';

document.addEventListener('DOMContentLoaded', async function () {
    const currentPath = window.location.pathname;

    if (currentPath === CONFIG.paths.indexView) {
        document.querySelector('.nearby-schools-container').innerHTML = '<p>Loading...</p>';
        
        const params = await initializeParams();
        setUpDynamicFilters(params, currentPath);

        fetchAndDisplayNearbyCourses(params);

    } else if (currentPath === CONFIG.paths.newSchoolView) {
        const autoCompleteContainer = document.getElementById("autocomplete");
        const locationInput = document.getElementById("id_location");
        const latitudeInput = document.getElementById("id_latitude");
        const longitudeInput = document.getElementById("id_longitude");

        const autoCompleteInput = new autocomplete.GeocoderAutocomplete(
            autoCompleteContainer, 
            CONFIG.apiKey, 
            { /* Geocoder options */ });
            autoCompleteInput.on('select', (location) => {
                if (location.properties) {
                    console.log(location)
                    const address = location.properties.formatted;
                    const coordinates = parseFloat(location.properties);
                    locationInput.value = address;
                    latitudeInput.value = latitude;
                    longitudeInput.value = longitude;
                    console.log(`${coordinates}`);                }
            });
        



    } else if (currentPath === CONFIG.paths.myCoursesView) {
        // fetch courses using user id and return all courses created with this id
        // Display courses created by user
        const id = document.querySelector('.user-id').innerHTML
        const url = `courses/get?${encodeURIComponent('created_by')}=${encodeURIComponent(id)}`
        fetchAndRender(url, currentPath)

    } else if (currentPath.startsWith('/course/') && currentPath.endsWith('/participants')) {
        const printButton = document.getElementById('print-button')
        const content = document.getElementById('printable-body')
        
        printButton.addEventListener('click', () => {
            console.log('click')
            html2pdf()
            .set({
                margin: 1,
                filename: 'participants.pdf',
                image: { type: 'jpeg', quality: 0.98 },
                html2canvas: { scale: 2 },
                jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
            })
            .from(content)
            .save();
        })
    } else if (currentPath === CONFIG.paths.teachersView) {
        const fetchUrl = ('/teachers/get')
        fetchAndRender(fetchUrl, currentPath)
        
    } else if (currentPath === CONFIG.paths.schoolsView) {
        const fetchUrl = ('schools/get')
        fetchAndRender(fetchUrl, currentPath)
    } 
});