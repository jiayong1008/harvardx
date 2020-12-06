from flask import redirect, render_template, request, session
from functools import wraps
from datetime import date, datetime



def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
        
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
    
    
def formattime(time):
    
    hour = time[0:2]
    
    if int(hour) == 0:
        formatted = "12" + time[2:5] + " AM"
    
    elif int(hour) < 10:
        start = hour[1:2]
        formatted = start + time[2:5] + " AM"
        
    elif int(hour) >= 10 and int(hour) < 12:
        formatted = hour + time[2:5] + " AM"
        
    elif int(hour) == 12:
        formatted = hour + time[2:5] + " PM"
        
    elif int(hour) > 12:
        start = str(int(hour) - 12)
        formatted = start + time[2:5] + " PM"
        
    return formatted
    
    
def countdays(initial_date):
    
    form_date = initial_date.split('-')
    form_date = date(int(form_date[0]), int(form_date[1]), int(form_date[2]))
    today = datetime.today().strftime('%Y-%m-%d').split('-')
    today = date(int(today[0]), int(today[1]), int(today[2]))
    difference = (form_date - today).days
    
    return difference