## Description  
This app is designed to help users find classes near their current location while allowing teachers to offer courses to them.  

The core functionality is centered on the homepage, where users can apply various filters to refine their search. Courses are displayed based on relevance and ranked by proximity to the user’s location. Students have the ability to register for courses, while teachers can manage their listings, including the option to delete them.  

Both students and teachers have access to a **MyCourses** tab, which provides a summary of their interactions. Students can view the courses they are enrolled in, while teachers see a list of the courses they have created.  


## Distinctiveness and Complexity  
This project is significantly larger and more complex than typical course projects, both in terms of size (lines of code, number of functions, and files) and complexity (geodata handling, multiple user types, external API calls, and database models). It also includes several advanced features such as filtering, animations, and downloadable content. To maintain clarity and modularity, JavaScript functionalities were divided across multiple files, ensuring that interactions between functions remained well-organized. A strong emphasis was placed on abstraction and loose coupling to make future modifications easier.  

The database models are more intricate, incorporating additional functionality. Notably, the School model utilizes geodata with point fields to store coordinates, requiring a more complex setup involving the PostGIS extension. This geospatial data is leveraged in views to perform radius-based queries and filtering. To support this, multiple API endpoints were created with customized serializers to process and structure data efficiently. This project was also my first experience working with geospatial data, and I integrated external API calls to Geoapify to enhance location-based features.  

Beyond backend complexities, the app also depends on a dynamic URL structure and multiple templates that incorporate conditional rendering, authentication logic, and mobile responsiveness. From a visual perspective, considerable effort was put into designing animations tailored to specific interactions, such as displaying a loading spinner and implementing smooth fade-and-slide transitions. Special attention was given to ensuring these animations were reusable across different parts of the application. Additionally, mobile responsiveness was achieved using the Bootstrap framework, ensuring a seamless experience across devices.  

Several external libraries were integrated to enhance functionality. For instance, an HTML-to-PDF conversion library was included to generate downloadable documents, while Pillow was used to manage image fields in models. For development and testing, Faker and FactoryBoy were employed to generate realistic dummy data. These tools made it easier to populate the database and simulate various use cases.  

Finally, many aspects of the project were built with scalability in mind. As new features are added and data storage requirements evolve, the system has been designed to accommodate future refactoring. Functions and components were structured to remain as loosely coupled as possible. This approach ensures that the project remains maintainable and adaptable as it continues to grow.  


## Contents of Each File  
### models.py  
The project relies on three key models: User, Course, and School, each with its own set of properties and utility functions.  

Courses are linked to schools via a foreign key, a decision made to simplify data management. This setup allows for efficient queries that retrieve all courses offered by a given school. Instead of requiring teachers to manually enter an address for each course, they can simply select an existing school or create a new one. Additionally, this structure enables users to browse schools and see all courses provided at each location.  

Schools store their coordinates, which are fetched via the Geoapify API. These coordinates facilitate radius-based search, allowing users to find courses near their location. Since each Course is linked to a School, and each School contains its coordinates, filtering courses by distance is done by first finding nearby schools and then retrieving the courses they offer. This is made possible using GeoDjango’s PointField.  

The project also includes a custom user model that extends Django’s built-in AbstractUser. Instead of separate models for students and teachers, users are distinguished by a role property ('teacher' or 'student'). This single-model approach avoids redundancy since both roles share the same properties, differing only in the features they can access.  

### forms.py  
This project makes use of multiple forms:  
- A customized Django user creation form for registration.  
- A Django login form to allow authentication.  
- A custom course form for the teachers to create new classes.  
- A school form to create new schools that includes an address field, which dynamically interacts with the Geoapify API to validate and fetch coordinates.  

Some forms inherit from Django’s built-in form classes, while others are model-based. Creating forms based on models allows data to be saved efficiently with minimal code.  

### views.py, serializers.py, middleware.py  
The app makes extensive use of fetch requests to retrieve data either from the project database or from Geoapify’s servers. On the frontend, these fetch calls enable dynamic rendering of database content, real-time filtering of courses, and validation of user-inputted addresses in the school creation form. If an address is valid, its coordinates are automatically fetched and stored upon form submission. On the backend, dedicated API endpoints were created to serve data for teachers, schools, and courses. These endpoints rely on custom serializers, ensuring that data is returned in a structured and properly formatted way.  

Django’s built-in mailing system was integrated to improve communication within the app. Whenever a student registers for a course, they receive a confirmation email, and the teacher is notified of the new enrollment. Additionally, if a teacher decides to delete a course, all registered students receive an email informing them of the cancellation. This ensures that users stay updated on course availability without needing to constantly check the app.  

One of the key features of the app is its location-based browsing system, allowing users to find courses near them. The views implement a distance filter, which takes the user’s location (retrieved dynamically when they visit the homepage) and a radius value set via the frontend filters. The app then queries the database to find nearby schools within that radius and retrieves the courses associated with them. This approach allows users to refine their search based on location, and once results are displayed, an additional search bar appears dynamically, enabling even more granular filtering.  

To improve stability and usability, error handling is an essential part of the views. Instead of cluttering individual views with repetitive error-handling logic, a custom middleware file was created to catch common errors and provide meaningful feedback using appropriate HTTP response codes. This not only makes the views cleaner and more readable but also ensures that errors are consistently handled across the application.  

### validators.py  
This file contains a custom validator that ensures address validity in the backend, complementing the frontend address validation using Geoapify.  

### management/commands/populate.py and tests/factories.py  
To automate dummy data generation, I created scripts that populate the database using the Faker and FactoryBoy libraries. These scripts can be executed via a custom management command (`populate.py`), making it easy to test the app with realistic data.  


## JS Files
- **main.js** – The entry point of the application. It initializes parameters, manages view-specific setups, and calls necessary functions based on the current page.
- **animation.js** – Handles UI animations, such as displaying a loading spinner while fetching data and adding smooth fade-and-slide transitions for showing or hiding containers.
- **csrfUtil.js** – Manages CSRF token retrieval and cookie handling for secure requests.
- **domUtils.js** – Provides helper functions for DOM manipulation, such as showing/hiding elements and rendering fetched data.
- **fetchUtils.js** – Contains functions for retrieving data from the database and conditionally displaying results based on the fetched content.
- **filterAndSearchUtils.js** – Handles all filtering and search-related logic, including dynamic filtering and user input processing.
- **geoUtils.js** – Manages geolocation-related functionality, such as retrieving user coordinates.
- **config.js** – Stores global constants like API paths and keys for easy access throughout the project.
- **downloadUtils.js** – Provides functionality for downloading content, including generating PDFs. A key feature of this project is allowing teachers to view a list of course participants (names and email addresses) and download a printable version.
- **elementFactories.js** – Simplifies Bootstrap element creation and assigns necessary data dynamically.

## How to Run the App
### 1. Setup
- Install the required dependencies.
- Start the server.

### 2. Navigation & Access
- The app starts on the index page.
- It can be used with or without logging in, but some features require registration and login.

### 3. Course Selection & Enrollment
- Users can apply filters to find relevant courses.
- Clicking on a course opens a detailed course page.
- Users can register for a course, while course creators can delete their own courses.
- In both cases, an email notification is sent to the relevant people.

### 4. My Courses Page
- Both students and teachers have access to a "My Courses" page, but it displays different information:
  - Students see a list of courses they are enrolled in.
  - Teachers see a list of courses they provide.
- Both students and teachers can select a course to open its page and perform additional actions.