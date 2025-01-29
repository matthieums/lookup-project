import { initializeParams } from './filterAndSearchUtils.js';
import { CONFIG } from './config.js';
import { fetchAndDisplayNearbySchools } from './fetchUtils.js';
import { setUpDynamicFilters } from './filterAndSearchUtils.js';
import { fetchAndRender, fetchAndDisplayClosestCityName } from './fetchUtils.js';

document.addEventListener('DOMContentLoaded', async function () {
    const currentPath = window.location.pathname;

    if (currentPath === CONFIG.paths.indexView) {
        const params = await initializeParams();
        fetchAndDisplayClosestCityName(params);
        setUpDynamicFilters(params, currentPath);
        fetchAndDisplayNearbySchools(params);

    } else if (currentPath === CONFIG.paths.newSchoolView) {
        const autoCompleteContainer = document.getElementById("autocomplete");
        const locationInput = document.getElementById("id_location");
        const latitudeInput = document.getElementById("id_latitude");
        const longitudeInput = document.getElementById("id_longitude");

        const autoCompleteInput = new autocomplete.GeocoderAutocomplete(
            autoCompleteContainer, 
            CONFIG.apiKey, 
            {  filter: { country: "BE" }  });
            autoCompleteInput.on('select', (location) => {
                if (location.properties) {
                    const address = location.properties.formatted;
                    locationInput.value = address;
                    latitudeInput.value = latitude;
                    longitudeInput.value = longitude;          
                }
            });
            document.querySelector('.geoapify-close-button').classList.add('d-none')
            document.querySelector('.geoapify-autocomplete-input').classList.add('form-control')

    } else if (currentPath === CONFIG.paths.myCoursesView) {
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
    }
});