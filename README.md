# MasterTime
A time planner application designed to help users efficiently and effectively schedule days or weeks ahead. Users will be able to register, login, customize weekly schedule (add, edit, delete), add special events, modify to-do list, and of course, logout.

## Specifications
This project has been implemented using Python Flask, HTML, CSS, JavaScript, SQLite, and Bootstrap. Laid out as below are the list of specification in this project:

- **Registration, Login, Logout:** Users shall be able to register for an account, login, logout, and modify their password if they wish to.
- **Weekly Schedule:** Signed in users shall be able to plan weekly timetable, where activities within this timetable occurs every week. This can be but not limited to work or school schedule. 
- **Special Events:** Users can schedule a date for a 'special event' which doesn't quite fit in the weekly schedule. E.g. dental appointment, special meetings, etc.
- **To-do List:** Users will be able to add multiple tasks, and 'complete' the task once finished.

## Files and Directories
This code consists of a Flask project which has a main app, `application.py`.

- `application.py` - 
- `helpers.py` - Contains helper functions used in `application.py`.
- `static` - Composed of static files.
    - `javascript.js` - JavaScript for front end.
    - `styles.css` - Web page stylings.
- `templates` - Consist of HTML templates for different pages.
    - ```layout.html``` - Layout template, other templates extends it.
    - ```index.html``` - Template for Home page
    - ```login.html``` - Login template
    - ```register.html``` - Registeration template
    - ```schedule.html``` - Schedule template
    - ```todo.html``` - To-do list template
    - ```events.html``` - Special events template
    - ```change.html``` - Change Password template
    - ```apology.html``` - Display error template
- `project.db` - SQLite database storing all data within this project.
- `README.md` - Describes this project.
- `requirements.txt` - Installed Python packages. 

## Installation
1. Run `pip install -r requirements.txt` to install all project dependencies.
2. Execute `export FLASK_APP=application` (use `set` instead of `export` for Windows).
3. Run `flask run` to startup the Flask server.