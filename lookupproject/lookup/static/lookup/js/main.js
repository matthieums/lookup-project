// Globals
var path = window.location.pathname;
const indexView = '/'
const teachersView = '/teachers'
const newSchoolView ='/newschool'
const schoolsView = '/schools'
const contactView = '/contact'
const locationBasedBrowser = '/geoschool'
const participantsView = '/participants'
const myCoursesView = '/mycourses'
// If I change the API key, make sure I change it in the validators.py file too
const ApiKey = '931a2f65384241b19147a6b601733f10'

document.addEventListener('DOMContentLoaded', function () {
//     getUserCoordinates()
//         .then((coords) => {
//             console.log('User Coordinates:', coords)
//         })
//         .catch((error) => {
//             console.error(error);
//         })

    if (path === indexView) {
        document.querySelector('.nearby-schools-container').innerHTML = '<p>Loading...</p>';

        // Development data
        const userCoordinates = [51.18, 4.4];
        const radius_in_meters = 1000

        fetchAndDisplayNearbySchools(userCoordinates, radius_in_meters)

        // Prepare the fetch request with the appropriate parameters. 
        const formSelects = Array.from(document.querySelectorAll('.form-select'));
        let params = {
            discipline: null,
            age_group: null,
            radius: radius_in_meters,
            user_lon: userCoordinates[0],
            user_lat: userCoordinates[1]
        }

        formSelects.forEach((selectForm) => {
            selectForm.addEventListener('change', function (event) {
                document.querySelector('.results-container').innerHTML = 'LOADING...'
                const value = event.target.value;
                const selectType = selectForm.getAttribute('aria-label');
                params[selectType] = value ? value : null;
                
                const queryString = Object.entries(params)
                .filter(([key, value]) => value !== null && value !== "")
                .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
                .join('&');

                const fetchUrl = `courses/get?${queryString}`;
                fetchAndRender(fetchUrl);
            })
        })

    } else if (path === newSchoolView) {
        const autoCompleteContainer = document.getElementById("autocomplete");
        const locationInput = document.getElementById("id_location");
        const latitudeInput = document.getElementById("id_latitude");
        const longitudeInput = document.getElementById("id_longitude");

        const autoCompleteInput = new autocomplete.GeocoderAutocomplete(
            autoCompleteContainer, 
            ApiKey, 
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
        



    } else if (path === myCoursesView) {
        // fetch courses using user id and return all courses created with this id
        // Display courses created by user
        const id = document.querySelector('.user-id').innerHTML
        const url = `courses/get?${encodeURIComponent('created_by')}=${encodeURIComponent(id)}`
        fetchAndRender(url)

    } else if (path.startsWith('/course/') && path.endsWith('/participants')) {
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
    } else if (path === teachersView) {
        const fetchUrl = ('/teachers/get')
        fetchAndRender(fetchUrl)
        
    } else if (path === schoolsView) {
        const fetchUrl = ('schools/get')
        fetchAndRender(fetchUrl)
    } 


    // Fetch data and call function to display data
    function fetchAndRender(url) {
        fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error')
            }
            return response.json();
        })
        .then(data => renderResults(data))
        .catch(error => {
            console.log('error', error)
        })
    }

    // Renders data and adds a search bar
    function renderResults(data) {
        const resultsContainer = document.querySelector('.results-container')

        let containersToHide = [];
        
        if (path === indexView) {
            const nearbySchoolsContainer = document.querySelector('.nearby-schools-container')
            const submitCourseContainer = document.querySelector('.submit-course-container');
            const categoriesContainer = document.querySelector('.categories-container');    
            containersToHide.push(categoriesContainer, submitCourseContainer, nearbySchoolsContainer);
        } else if (path === teachersView) {
            const teacherContainer = document.querySelector('.teacher-container')
            containersToHide.push(teacherContainer)
        }

        hideUnnecessaryContainers(containersToHide)

        if (path === indexView) {
            formatResultsAsCards(data)
            const searchBar = searchBarFactory()
            resultsContainer.prepend(searchBar);
        } else if (path === myCoursesView) {
            formatResultsAsTable(data)
        } else if (path === teachersView) {
            formatResultsAsStrings(data)
            const searchBar = searchBarFactory()
            resultsContainer.prepend(searchBar);
        } else if (path === schoolsView) {
            formatResultsAsStrings(data)
            const searchBar = searchBarFactory()
            resultsContainer.prepend(searchBar);
        }


    }

    function formatResultsAsStrings(data) {
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

    function formatResultsAsCards(data) {
        const resultsContainer = document.querySelector('.results-container');
        resultsContainer.innerHTML = '';

        data.forEach((object) => {
            const card = document.createElement('div');
    
            const header = object.name;
            const title = object.teacher;
            const text = object.description;
            const footer = object.target_audience;

            const cardBody = courseCardFactory(header, title, text, footer);
            card.appendChild(cardBody);
            resultsContainer.append(cardBody);
        })
    }

    function hideUnnecessaryContainers(containers) {
        containers.forEach(container => {
            container.classList.add('d-none')
        })
    }

    function formatResultsAsTable(data) {
        // TO-DO: Make more reusable. This function is only usable on one type of data. 
        const tableBody = document.querySelector('.table-body')
        tableBody.innerHTML = ''

        data.forEach(({ id, name, students, place, schedule }) => {
            const row = document.createElement('tr');
            let studentCount = students.length;
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

        })
    }


    function searchBarFactory() {
        const searchBar = document.createElement('input');
        searchBar.type = 'text'
        searchBar.placeholder = 'Search here'
        searchBar.classList.add('search-bar')

        searchBar.addEventListener('keyup', function(event) {
            const searchQuery = event.target.value
                narrowResults(searchQuery)
        })
        return searchBar;
    }

    function narrowResults(searchQuery) {
        const allResults = document.querySelectorAll('.result')
        const normalizedQuery = searchQuery.toLowerCase()

        allResults.forEach(result => {
            let resultData;

            if (result.classList.contains('card')) {
                resultData = result.firstElementChild.textContent
            } else {           
                resultData = result.textContent
            }

            if (!resultData.toLowerCase().startsWith(normalizedQuery)) {
                result.classList.add('d-none')
            } else {
                result.classList.remove('d-none')
            }
        })
    }

    // Allows for the creation of cards with appropriate data.
    // I add the result class so it can be manipulated dynamically
    function courseCardFactory(header, title, text, footer) {
        const card = document.createElement('div');
        card.classList.add('card', 'text-center', 'm-4', 'result');

        const cardHeader = document.createElement('div');
        cardHeader.classList.add('card-header');
        cardHeader.textContent = header;

        const cardBody = document.createElement('div');
        cardBody.classList.add('card-body');

        const cardTitle = document.createElement('h5');
        cardTitle.classList.add('card-title');
        cardTitle.textContent = title;

        const cardText = document.createElement('card-text');
        cardText.classList.add('card-text');
        cardText.textContent = text;

        const cardFooter = document.createElement('div');
        cardFooter.classList.add('card-footer', 'text-body-secondary');
        cardFooter.textContent = footer

        card.append(cardHeader, cardBody, cardTitle, cardText, cardFooter);

        return card
    }



    // Function to get CSRF token (required for Django's CSRF protection)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    async function fetchAndDisplayNearbySchools(coordinates, radius) {
        fetch('/geoschool', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') },
            body: JSON.stringify({ 
                user_lat: coordinates[0],
                user_lon: coordinates[1],
                radius: radius
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('NETWORK RESPONSE WAS NOT OK')
            }
            return response.json();
        })
        .then(data => {
            const nearbySchoolsContainer = document.querySelector('.nearby-schools-container');
            nearbySchoolsContainer.innerHTML = '';
    
            if (data.error) {
                nearbySchoolsContainer.innerHTML = `${data.error}`;
            } else {
                data.forEach(school => {
                    nearbySchoolsContainer.innerHTML += school.name;
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.querySelector('.nearby-schools-container').innerHTML = 'AN ERROR HAS OCCURED';
        });
    
    }
   
    function getUserCoordinates() {
        return new Promise((resolve, reject) => {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        resolve [position.coords.latitude, position.coords.longitude];
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

});