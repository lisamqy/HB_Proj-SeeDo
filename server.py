
from flask import Flask, session, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db
import crud
from jinja2 import StrictUndefined
from random import sample

app = Flask(__name__)
app.secret_key = 'secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.jinja_env.undefined = StrictUndefined

# API_KEY = os.environ['TICKETMASTER_KEY']


@app.route("/")
def homepage():
    """Show homepage."""

    if "current_user" in session:
        user = crud.get_user_by_id(session["current_user"])
    else: 
        user = None
    events = sample(crud.get_events(),10)

    return render_template("homepage.html", user=user, events=events) 
    

@app.route("/handle-login", methods=["POST"])
def handle_login():
    """Log user into application"""   

    email = request.form["email"]
    password = request.form["password"]    
    user = crud.get_user_by_email(email) #communicates with db to grab existing users info from db

    if user and password == user.password: #checks against database
        session["current_user"] = user.user_id #saves the current user's user_id in session
        flash(f'Logged in as {user.username}') 
        return redirect("/")
    else:
        flash("Email or password incorrect, please try again.")
        return redirect("/")


@app.route("/goodbye")   
def logout():
    """Clear the session and return to homepage"""

    session.clear()
    return redirect("/")


@app.route("/new") 
def new_user():
    """Creates a new user for application"""

    return render_template("register.html")


@app.route("/new", methods=["POST"]) 
def create_user():
    """Creates a new user for application"""

    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"] 
    crud.create_user(username, email, password) #communicates with db to add in new user

    return redirect("/")


@app.route("/user/<user_id>")
def user_page(user_id):
    """Show user's account details"""

    user = crud.get_user_by_id(user_id)
    plans = crud.get_plans(user_id)

    return render_template("accountdetails.html", user=user, plans=plans)


@app.route("/user/<user_id>", methods=["POST"])
def add_plan(user_id):
    """Show user's account details"""

    location_id = request.form.get("location_id")
    crud.create_plan(user_id=user_id,location_id=location_id,overview=None)

    return redirect(f"/user/{user_id}")
    

@app.route("/plan/<plan_id>")    
def plan_page(plan_id):
    """Show a specific plan's details"""

    db_events = crud.get_events() #dropdown event items
    events = crud.get_events_associated_with_plan(plan_id) 
    plan = crud.get_plan_by_planid(plan_id)

    location_id = crud.get_location_by_planid(plan_id)
    location = crud.get_location_by_id(location_id)

    return render_template("plandetails.html", db_events=db_events, events=events, plan=plan, location=location)


@app.route("/plan/<plan_id>", methods=["POST"])
def add_event(plan_id):
    """Add event to current plan"""

    event_id = request.form.get("dropdown-event")
    crud.add_plan_events(plan_id=plan_id, event_id=event_id)

    return redirect(f"/plan/{plan_id}")
    

@app.route("/event/<event_id>")
def event_page(event_id):
    """Show an event's details"""

    event = crud.get_event_by_id(event_id)
    location = crud.get_location_by_id(event.location_id)
    all_theme = crud.get_theme()
    theme = sample(all_theme,3)

    return render_template("eventdetails.html", event=event, location=location, theme=theme)


if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0")
