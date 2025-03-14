import { CONFIG } from './config.js';


/**
 * Fetches the user's coordinates, or returns default coordinates if the location can't be fetched.
 * @returns {Promise<Array<number>>} A promise that resolves to an array of [latitude, longitude].
 */
export async function initializeUserCoordinates() {
    let userCoordinates;

    try {
        userCoordinates = await getUserCoordinates();
        return userCoordinates

    } catch(error) {
        userCoordinates = [51.18, 4.4];
        return userCoordinates

    }
}

/**
 * Retrieves the user's geolocation.
 * @returns {Promise<Array<number>>} Resolves to an array of [latitude, longitude].
 */
function getUserCoordinates() {
    return new Promise((resolve, reject) => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    resolve([position.coords.latitude, position.coords.longitude]);
                },
                (error) => {
                    reject('Error getting location' + error.message);
                }
            );
        } else {
            reject('Geolocation is not supported by this browser');
        }
    });
}

export function createGeocoderAutocomplete(container) {
    const autoCompleteInput = 
    new autocomplete.GeocoderAutocomplete(
        container, 
        CONFIG.apiKey, 
        {  filter: { country: "BE" }  });

        setupGeocoderAutocomplete(autoCompleteInput)
}

function setupGeocoderAutocomplete(input) {
    const locationInput = document.getElementById("id_location");
    const coordinatesInput = document.getElementById("id_coordinates");

    input.on('select', (location) => {
        if (location.properties) {
            const address = location.properties.formatted;
            const latitude = location.properties.lat;
            const longitude = location.properties.lon; 
            locationInput.value = address;
            coordinatesInput.value = `${longitude},${latitude}`;
        }
    });
    document.querySelector('.geoapify-close-button').classList.add('d-none');
    document.querySelector('.geoapify-autocomplete-input').classList.add('form-control');
}