# TravelHypes
Trip planner website for planning trips to specific country in advance. Users will be able to register for an account, create a customized daily itinerary based on suggestions from API, share their itinerary to public, view or clone someone else's itinerary, and of course, delete individual destination from a trip or delete the entire trip made by themselves if they wish to.

## Distinctiveness and Complexity
This project utilizes API both on the frontend and backend. Backend API ([Windy API](https://api.windy.com/webcams/docs/)) allows the web page to gain access to webcams worldwide which would then be displayed to users. This assists users in making a better decision through the real time images provided by the API.

## Specification
This project is fully mobile-responsive and is implemented using Python Django, JavaScript, HTML, CSS, Bootstrap, and [Windy API](https://api.windy.com/webcams/docs/). Listed below are the list of specification in this project:

- **Registration, Login, Logout**: Users can register for an account, log in, and log out from the web page.
- **New Trip**: Signed in users are allowed to create new trip by filling up a form available within the home page.
- **View Trip**: Users who are not signed in can view a list of public trips. Signed in users are allowed to view trips made by themselves as well as public trips. Trips are displayed in reverse chronological order.
    - Clicking on individual trips will load the specific trip.
    - Each trip is broken down to day by day itinerary.
    - Each day consists of different destinations with different durations (empty by default).
- **Add Destinations**: Trip owner can add destination to their itinerary by clicking on the 'Add Destination' button.
    - Clicking this button loads a list of places (ordered by popularity) with real time images shown (information obtained from API).
    - Users can add any of these destinations to their day by day itinerary.
    - Added destinations can be removed from their itinerary later on.
- **Privacy**: Trip owners are allowed to make trips public or private by clicking on the "Make it Public" or "Keep it Private" button displayed to them when they are viewing individual trips. "Public" trips will be visible to all users, whereas "private" trip are only visible to themselves.
- **Clone / Delete Trip**: Trip owner can delete individual trip any time. Any other signed in users are allowed to clone trips made by someone else (provided the trip is set to "public").
- **Pagination**: For pages that displays trips or place recommendations, appropriate number of items are displayed at once. Users can move to the "Next" page or "Previous" page (if exist) to view more trips / places.

## Files and Directories
This code consists of a Django project known as ```travel``` which has an app known as ```planner```.
- ```planner``` - Main application.
    - ```static/planner``` - Consists of static files.
        - ```index.js``` - JavaScript for front end.
        - ```nature.jpg``` - Background image for front end.
        - ```styles.css``` - Takes care of web page's stylings.
    - ```templates/planner``` - Consist of HTML templates for different pages.
        - ```layout.html``` - Layout template, other templates extends it.
        - ```index.html``` - Template for Home page and 'My Trip' page
        - ```login.html``` - Login template
        - ```register.html``` - Registeration template
        - ```trip.html``` - Template which displays user's current itinerary or displays real time webcams to users (depend on views).
    - ```admin.py``` - Register models to Django admin application.
    - ```models.py``` - Contains all models within this app.
    - ```urls.py``` - Contains URL configurations for this app.
    - ```views.py``` - Contains all views within this app.
- ```travel``` - Default application created by Django.
- ```db.sqlite3``` - Default database created upon running ```migrate``` command.
- ```manage.py```- Command-line utility for executing Django commands.
- ```README.md``` - Describes this project.
- ```requirements.txt``` - Installed Python packages.

Note: Some built in files such as ```__init__.py```, ```apps.py```, ```tests.py``` are not mentioned above as it has not been modified.

## Installation
1. Run ```pip install -r requirements.txt``` to install all project dependencies.
2. Run ```python manage.py makemigrations``` and  ```python manage.py migrate``` to make and apply all migrations.
3. Run ```python manage.py runserver``` to startup the Django server.