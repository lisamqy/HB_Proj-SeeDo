
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
        return render_template("homepage.html")
    else:
        flash("Wrong password!")
        return redirect("/login")


# @app.route("/rsvp", methods=['POST'])
# def rsvp():
#     """Register for the party."""

#     name = request.form.get("name")
#     email = request.form.get("email")

#     session['RSVP'] = True
#     flash("Yay!")
#     return redirect("/")


# @app.route("/games")
# def games():
#     games = Game.query.all()
#     return render_template("games.html", games=games)


if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0")
