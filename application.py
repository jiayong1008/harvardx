from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash


from helpers import apology, login_required, formattime, countdays

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.route("/")
@login_required
def index():
    
    # schedule table
    rows = db.execute("""SELECT start, end, title, day FROM schedules 
                         WHERE user_id = :id ORDER BY dayvalue, start""",
                         id = session["user_id"])

    schedules = []

    for i in range(len(rows)) :

        formatted_start = formattime(rows[i]["start"])
        formatted_end = formattime(rows[i]["end"])
        schedules.append({ "start": rows[i]["start"], "end": rows[i]["end"],
                            "title": rows[i]["title"], "day": rows[i]["day"],
                            "formatted_start": formatted_start, "formatted_end": formatted_end,
                            "index": i })
    
    # Special events table                        
    lines = db.execute("""SELECT date, title FROM events
                           WHERE user_id = :id ORDER BY date""",
                           id = session["user_id"])
                           
    events = []
    
    for row in lines:

        difference = countdays(row["date"])
        events.append({ "date": row["date"], "title": row["title"], "difference": difference })
        
        
    # To-Dos Table
    tasks = db.execute("""SELECT date, task FROM todos WHERE user_id = :id 
                         AND complete = '0' ORDER BY date""",
                         id = session["user_id"])
        
    todos = []
    
    for row in tasks:
        
        difference = countdays(row["date"])
        todos.append({ "date": row["date"], "task": row["task"], "difference": difference })

    return render_template("index.html", schedules=schedules, events=events, todos=todos)
    

@app.route("/schedule", methods=["GET", "POST"])
@login_required
def schedule():

    if request.method == "POST":

        title = request.form.get("title")
        start_time = request.form.get("start")
        end_time = request.form.get("end")
        days = request.form.getlist('day')

        for day in days:

            if day == "Sunday":
                value = 1
            elif day == "Monday":
                value = 2
            elif day == "Tuesday":
                value = 3
            elif day == "Wednesday":
                value = 4
            elif day == "Thursday":
                value = 5
            elif day == "Friday":
                value = 6
            elif day == "Saturday":
                value = 7

            db.execute("""INSERT INTO schedules (user_id, start, end, title, day, dayvalue)
                          VALUES (:user_id, :start, :end, :title, :day, :dayvalue)""",
                          user_id = session["user_id"], start = start_time, end = end_time,
                          title = title, day = day, dayvalue = value)

        flash("Added!")
        return redirect("/schedule")

    else:

        rows = db.execute("""SELECT start, end, title, day
                             FROM schedules WHERE user_id = :id
                             ORDER BY dayvalue, start""",
                             id = session["user_id"])

        schedules = []

        for i in range(len(rows)) :

            formatted_start = formattime(rows[i]["start"])
            formatted_end = formattime(rows[i]["end"])
            schedules.append({ "start": rows[i]["start"], "end": rows[i]["end"],
                                "title": rows[i]["title"], "day": rows[i]["day"],
                                "formatted_start": formatted_start, "formatted_end": formatted_end,
                                "index": i })

        return render_template("schedule.html", schedules=schedules)


@app.route("/deleteall", methods=["POST"])
@login_required
def deleteall():

    if request.method == "POST":

        # Delete all schedules
        if request.form.get("schedule"):
            
            db.execute("DELETE FROM schedules WHERE user_id = :id",
                        id = session["user_id"])
    
            flash("Deleted all Schedules!")
            return redirect("/schedule")
        
        # Delete all events   
        elif request.form.get("event"):
            
            db.execute("DELETE FROM events WHERE user_id = :id",
                        id = session["user_id"])
    
            flash("Deleted all Special Events!")
            return redirect("/events")
            
        elif request.form.get("todo"):
            
            db.execute("DELETE FROM todos WHERE user_id = :id",
                        id = session["user_id"])
            
            flash("Deleted all Tasks!")
            return redirect("/todo")


@app.route("/edit", methods=["POST"])
@login_required
def edit():

    if request.method == "POST":

        day = request.form.get("day")
        start = request.form.get("start")
        end = request.form.get("end")
        title = request.form.get("title")
        
        print(day, start, end, title)

        newtitle = request.form.get("newtitle")
        newstart = request.form.get("newstart")
        newend = request.form.get("newend")

        db.execute("""UPDATE schedules SET title = :title, start = :start, end = :end
                      WHERE user_id = :id AND day = :day AND start = :initialStart AND
                      end = :initialEnd AND title = :initialTitle""",
                      title=newtitle, start=newstart, end=newend, id = session["user_id"],
                      day=day, initialStart=start, initialEnd=end, initialTitle=title)

        #UPDATE schedules SET title = "Math Lecture", start = "08:30", end = "10:30"
        # WHERE user_id = "1" AND day = "Monday" AND start = "08:32" AND
        # end = "14:00" AND title = "Maths Lecture";

        flash("Schedule Has Been Updated!")
        return redirect("/schedule")


@app.route("/delete", methods=["POST"])
@login_required
def delete():

    if request.method == "POST":

        if request.form.get("schedule"):
            
            day = request.form.get("day")
            start = request.form.get("start")
            end = request.form.get("end")
            title = request.form.get("title")
            
            db.execute("""DELETE FROM schedules WHERE user_id = :id
                          AND day = :day AND start = :initialStart AND
                          end = :initialEnd AND title = :initialTitle""",
                          id = session["user_id"], day=day, initialStart=start, 
                          initialEnd=end, initialTitle=title)
    
            flash("Deleted Schedule!")
            return redirect("/schedule")
            
        elif request.form.get("event"):
            
            date = request.form.get("date")
            title = request.form.get("title")
            
            db.execute("""DELETE FROM events WHERE user_id = :id
                          AND date = :date AND title = :title""",
                          id = session["user_id"], date=date, title=title)
                          
            flash("Deleted Event!")
            return redirect("/events")
            
        elif request.form.get("todo"):
            
            task = request.form.get("task")
            date = request.form.get("date")
            
            db.execute("""DELETE FROM todos WHERE user_id = :id
                          AND task = :task AND date = :date""",
                          id = session["user_id"], task=task, date=date)
            
            flash("Deleted Task!")
            return redirect("/todo")


@app.route("/events", methods=["GET", "POST"])
@login_required
def events():
    
    if request.method == "POST":
        
        form_date = request.form.get("date")
        title = request.form.get("title")
        
        db.execute("""INSERT INTO events (user_id, date, title)
                      VALUES (:user_id, :date, :title)""",
                      user_id=session["user_id"], date=form_date, title=title)
        
        flash("Added!")
        return redirect("/events")
    
    else:
        
        rows = db.execute("""SELECT date, title FROM events
                             WHERE user_id = :id ORDER BY date""",
                             id = session["user_id"])
        
        events=[]                      
        for row in rows:

            difference = countdays(row["date"])
            events.append({ "date": row["date"], "title": row["title"], "difference": difference })
        
        return render_template("events.html", events=events)
        
        
@app.route("/todo", methods=["GET", "POST"])
@login_required
def todo():
    
    if request.method == "POST":
        
        task = request.form.get("task")
        date = request.form.get("date")
        
        if request.form.get("add"):
            
            #TODO
            db.execute("""INSERT INTO todos (user_id, task, date, complete)
                          VALUES (:user_id, :task, :date, :complete)""",
                          user_id=session["user_id"], task=task, date=date, 
                          complete = '0')
                          
            flash("Added!")
            return redirect("/todo")
            
        elif request.form.get("complete"):
            
            #TODO
            db.execute("""UPDATE todos SET complete = '1'
                          WHERE user_id = :id AND task = :task AND date = :date""",
                          id = session["user_id"], task=task, date=date)
                          
            flash("Updated!")
            return redirect("/todo")
        
    else:
        
        rows = db.execute("""SELECT date, task FROM todos WHERE user_id = :id 
                              AND complete = '0' ORDER BY date""",
                              id = session["user_id"])
        
        todos = []
        
        for row in rows:
            
            difference = countdays(row["date"])
            todos.append({ "date": row["date"], "task": row["task"], "difference": difference })
                              
        completes = db.execute("""SELECT date, task FROM todos WHERE user_id = :id 
                                  AND complete = '1' ORDER BY date""",
                                  id = session["user_id"])
                              
        return render_template("todo.html", todos=todos, completes=completes)
    

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        username = username.split()

        if len(username) != 1:
            return apology("must provide username with no space in between", 403)
        elif not username:
            return apology("must provide username", 403)
        elif not password:
            return apology("must provide password", 403)
        elif not confirmation:
            return apology("must provide confirmation password", 403)
        # elif len(password) < 6:
        #     return apology("password must consist of at least 6 characters", 403)
        elif password != confirmation:
            return apology("password and confirmation password does not match", 403)

        rows = db.execute("SELECT * FROM users WHERE username = :username", username = username)

        if len(rows) != 0:
            return apology("Sorry, this username is already taken", 403)

        hashes = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hashes)",
                    username = username, hashes = hashes)

        flash("Registered!")
        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        flash("You can modify your tables in the 'Schedule', 'Special Events', or 'To-Do' tab!")
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# Change Password
@app.route("/change", methods = ["GET", "POST"])
@login_required
def change():
    """Change user's password"""

    if request.method == "POST":

        password = request.form.get("password")
        new_pass = request.form.get("newpass")
        confirmation = request.form.get("confirmation")

        if not password:
            return apology("Must provide current password", 403)
        elif not new_pass:
            return apology("Must provide new password", 403)
        elif not confirmation:
            return apology("Must provide confirmation password", 403)
        elif new_pass != confirmation:
            return apology("Password and confirmation password does not match", 403)
        elif password == new_pass:
            return apology("New password cannot be same as previous password", 403)

        rows = db.execute("SELECT hash FROM users WHERE id=:id",
                            id = session["user_id"])
        ori_hash = rows[0]["hash"]

        if not check_password_hash(ori_hash, password):
            return apology("Incorrect password provided", 403)

        new_hash = generate_password_hash(new_pass)
        db.execute("UPDATE users SET hash=:new_hash WHERE id=:id",
                    new_hash = new_hash, id = session["user_id"])

        flash("Password Changed!")
        return redirect("/")

    else:

        rows = db.execute("SELECT username FROM users WHERE id=:id",
                           id = session["user_id"])
        username = rows[0]["username"]

        return render_template("change.html", username=username)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)