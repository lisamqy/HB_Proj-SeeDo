
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
    
    if session:
        return render_template("homepage.html")

    return render_template("login.html")
    

@app.route("/handle-login", methods=["POST"])
def handle_login():
    """Log user into application"""   

    username = request.form["username"]
    password = request.form["password"]    

    if password == "123":
        session["current_user"] = username
        flash(f'Logged in as {username}') 
        return redirect("/")
    else:
        flash("Password incorrect, please try again.")
        return render_template("login.html")


@app.route("/new") 
def new_user():
    """Creates a new user for application"""

    return render_template("register.html")


@app.route("/user")
def user_page():
    """Show user's account details"""

    return render_template("accountdetails.html")

@app.route("/plan")    
def plan_page():
    """Show a specific plan's details"""

    return render_template("plandetails.html")




if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0")
