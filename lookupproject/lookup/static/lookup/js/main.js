import { initializeParams, setUpDynamicFilters } from './filterAndSearchUtils.js';
import { CONFIG } from './config.js';
import { fetchAndRender, fetchAndDisplayClosestCityName } from './fetchUtils.js';
import { createGeocoderAutocomplete } from './geoUtils.js';

document.addEventListener('DOMContentLoaded', async function () {
    const currentPath = window.location.pathname;

    if (currentPath === CONFIG.paths.indexView) {
        const params = await initializeParams();
        fetchAndDisplayClosestCityName(params);
        setUpDynamicFilters(params, currentPath);

    } else if (currentPath === CONFIG.paths.newSchoolView) {
        const autoCompleteContainer = document.getElementById("autocomplete");
        createGeocoderAutocomplete(autoCompleteContainer);

    } else if (currentPath === CONFIG.paths.myCoursesView) {
        const id = document.querySelector('.user-id').innerHTML;
        const url = `courses/get?${encodeURIComponent('created_by')}=${encodeURIComponent(id)}`;
        fetchAndRender(url, currentPath);

    } else if (currentPath.startsWith('/course/') && currentPath.endsWith('/participants')) {
        setupDownloadButton();
    }
});