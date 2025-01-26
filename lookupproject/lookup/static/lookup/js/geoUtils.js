

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
