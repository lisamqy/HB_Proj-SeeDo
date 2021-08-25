
from flask import Flask, session, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "secret"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def homepage():
    """Show homepage."""

    # plans = crud.get_plans()
    user = crud.get_user_by_id(3)
    events = crud.get_events(10)

    return render_template("homepage.html", user=user, events=events) #get first 10 plans from db
    

@app.route("/handle-login", methods=["POST"])
def handle_login():
    """Log user into application"""   

    email = request.form["email"]
    password = request.form["password"]    
    user = crud.get_user_by_email(email) #communicates with db to create new user

    if user and password == user.password: #checks against database
        session["current_user"] = user.username
        flash(f'Logged in as {user.username}') 
        return redirect("/")
    else:
        flash("Password incorrect, please try again.")
        return render_template("homepage.html")

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
    crud.create_user(username, email, password)

    return redirect("/")

@app.route("/user<user_id>")
def user_page(user_id):
    """Show user's account details"""

    plans = crud.get_plans(user_id)

    return render_template("accountdetails.html", plans=plans)

@app.route("/plan")    
def plan_page():
    """Show a specific plan's details"""

    events = crud.get_events(5)

    return render_template("plandetails.html", events=events)

@app.route("/event")
def event_page():
    """Show an event's details"""

    events = crud.get_events(5)

    return render_template("plandetails.html", events=events)


if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0")
