
from flask import Flask, session, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db
import crud
import helper
from pprint import pformat
import os
import requests
from jinja2 import StrictUndefined
from random import sample
from datetime import date

app = Flask(__name__)
app.secret_key = 'secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.jinja_env.undefined = StrictUndefined

API_KEY = os.environ['TICKETMASTERKEY']


@app.route("/")
def homepage():
    """Show homepage."""

    if "current_user" in session:
        user = crud.get_user_by_id(session["current_user"])
    else: 
        user = None
    events = sample(crud.get_events(),8)
    likes = []
    for event in events:
        
        like = crud.get_likes(event.event_id)
        likes.append(like)

    locations = crud.get_locations()

    return render_template("homepage.html", user=user, events=events, likes=likes, locations=locations) 
    

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


@app.route("/handle-likes", methods=['POST'])
def handle_likes():
    """Update an event's number of likes"""  
    
    user_id = session["current_user"]
    event_id = request.form.get("eventId")
    crud.add_like(user_id, event_id)
    return "Success"
    

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
    if crud.check_email_in_db(email) < 1:
        #communicates with db to add in new user
        crud.create_user(username, email, password) 
        flash("Success! Please log in.")
    else:
        flash("Email already in use, please try another.")
        return redirect("/new")

    return redirect("/")


@app.route("/user/<user_id>")
def user_page(user_id):
    """Show user's account details"""

    user = crud.get_user_by_id(user_id)
    plans = crud.get_plans(user_id)
    all_locations = crud.get_locations()
    liked = crud.get_user_liked(user_id)
    event_list = []

    #get a list of all events liked by current user; show event's overview
    for like in liked: 
        event_id = crud.get_event_by_id(like.event_id)  
        event_list.append(event_id)

    return render_template("accountdetails.html", user=user, plans=plans, all_locations=all_locations, event_list=event_list)


@app.route("/user/<user_id>", methods=["POST"])
def add_plan(user_id):
    """Create a new plan"""

    location_id = request.form.get("citynames")
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

@app.route("/plan/<plan_id>/overview", methods=["POST"])
def add_plan_overview(plan_id):
    """Edit overview for current plan"""

    overview = request.form.get("txtEditOverview")
    crud.edit_plan_overview(plan_id=plan_id, overview=overview)

    return redirect(f"/plan/{plan_id}")   

@app.route("/plan/<plan_id>/delete", methods=["POST"])
def del_current_plan(plan_id):
    """Delete current plan"""

    crud.del_plan_by_id(plan_id) 
    user_id = session["current_user"]

    return redirect(f"/user/{user_id}") 

@app.route("/plan/<plan_id>/delete/<event_id>")
def edit_plan_events(plan_id, event_id):
    """Delete events under current plan"""

    crud.del_from_planevent(event_id=event_id, plan_id=plan_id)

    return "Event deleted"     
      

@app.route("/event/<event_id>")
def event_page(event_id):
    """Show an event's details"""

    event = crud.get_event_by_id(event_id)
    location = crud.get_location_by_id(event.location_id)
    all_theme = crud.get_theme()
    likes = crud.get_likes(event_id)

    #check if user logged in, so we can then see if they've already liked the current event to decide which like button to show...
    if "current_user" in session: 
        user_id = session["current_user"]
        user_plans = crud.get_plans(user_id)
        like_count = crud.has_liked(user_id,event_id)
    #...if not logged in, guest will only see the liked #
    else:
        like_count = 1  
        user_plans = None  

    return render_template("eventdetails.html", event=event, location=location, user_plans=user_plans, likes=likes, like_count=like_count)

@app.route("/event/<event_id>/add", methods=['POST'])
def add_event_to_plan(event_id):
    """Adds current event to a user's plan"""

    event_id = event_id
    plan_id = request.form.get("plans")
    in_plan_count = crud.check_plan_event_dupe(plan_id=plan_id, event_id=event_id)
    if in_plan_count == 0:
        crud.add_plan_events(plan_id=plan_id, event_id=event_id)
    else:
        flash("Event already in plan.")
        return redirect(f"/event/{event_id}")

    print(f'\n\n{event_id},{plan_id}\n\n')
    return redirect(f"/plan/{plan_id}")


@app.route("/search")
def find_events():
    """Search for events on Ticketmaster"""

    keyword = request.args.get('keyword', '')
    city = request.args.get('city', '')
    collected_date = request.args.get('date', '')
    #in case user does not input date; set as today
    if collected_date == '':
        today = date.today()
        collected_date = today.strftime("%Y-%m-%d")
    startdate = collected_date+'T12:00:00Z'

    url = 'https://app.ticketmaster.com/discovery/v2/events'
    payload = {'apikey': API_KEY,
                'keyword': keyword,
                'city': city,
                'startDateTime': startdate,
                'sort': 'date,asc',
                'countryCode': 'US'}

    response = requests.get(url, params=payload)

    #edge case where user's query outputs 0 results
    if response.json()['page']['totalElements'] == 0:
        flash('0 Results found...Please try another query😥')
        return redirect("/")
    
    data = response.json()['_embedded']['events'] 
    events = helper.clean_search_results(data)

    #this makes sure if guest is browsing, it wont trigger an error trying to grab a user's plans on the event search results page
    if "current_user" in session:
        user_id = session["current_user"]
        user_plans = crud.get_plans(user_id)
    else: 
        user_plans = None

    return render_template('searchresults.html',
                           pformat=pformat,
                           data=data,
                           results=events,
                           user_plans=user_plans)


@app.route("/CreateAddEvent", methods=['POST'])
def create_add_event_to_plan():
    """Create and add the ticketmaster event to a user's plan"""

    cityname = request.form.get('city')
    loc_id = crud.get_loc_id_by_city(cityname)
    overview = request.form.get('overview')
    datetime = request.form.get('datetime')
    image_url = request.form.get('image')

    times_event_in_db = crud.existing_event(overview)
    #only create new event if it's not already in db
    if times_event_in_db < 1:
        new_event = crud.create_event(location_id=loc_id,overview=overview,datetime=datetime, image=image_url)
    
    event_id = crud.get_event_by_name(overview)

    user_id = session["current_user"]
    plan_id = request.form.get('plans')
    add_to_plan = crud.add_plan_events(plan_id, event_id)
    
    return redirect(f"/plan/{plan_id}")



if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0")
