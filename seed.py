"""Script to seed database."""

import os
import json
from random import choice, randint, sample
from datetime import datetime

import crud
import model
import server

os.system("dropdb project")
os.system("createdb project")

model.connect_to_db(server.app)
model.db.create_all()

# Create 10 users
for num in range(1,10):
    username = f"user{num}"
    email = f"user{num}@email.com"
    password = "123"

    user = crud.create_user(username,email,password)


# Load location data from JSON file
with open("data/locations.json") as f:
    location_data = json.loads(f.read())
# Create locations
locations_db = []
for location in location_data:
    statename, cityname, zipcode = (
        location["state"],
        location["cityname"],
        location["zipcode"]
    )
    countryname = "USA"

    location = crud.create_location(zipcode, cityname, statename)
    locations_db.append(location)


# Create x events
names = ["Amy", "Betty", "Charles", "Danny", "Ella", "Felicia", "George", "Hailey"]
events = ["birthday party", "pool party", "backyard BBQ", "hiking trip", "picnic trip", "virtual game night", "online workout", "paint night", "casino night", "art exhibit", "fireworks show", "scavenger hunt", "karaoke night"]

events_db = []
for name in names:
    location_id = randint(1,len(locations_db))
    x = choice(events)
    overview = f"{name}'s {x.title()}"
    datetime = datetime.now()

    event = crud.create_event(location_id, overview, datetime)
    events_db.append(event)



# Create some likes
for num in range(20):
    user_id = randint(1,9) #since we made 10 users above
    event_id = randint(1,len(events_db))

    likes = crud.add_like(user_id,event_id)

# Create x themes
with open("data/themes.json") as f:
    theme_data = json.loads(f.read())

themes_db = []
for theme in theme_data:
    tag = theme
    overview = f"the theme is related to: {theme}"

    theme = crud.create_theme(tag, overview)
    themes_db.append(theme)


# Create x plans
plan_list = []
for num in range(10):
    user_id = randint(1,9)
    location_id = randint(1,len(locations_db))

    plan = crud.create_plan(user_id,location_id)
    plan_list.append(plan)


# Add some events into a plan
for num in range(10):
    plan_id = randint(1,len(plan_list))
    event_id = randint(1,len(events_db))

    planevent = crud.add_plan_events(plan_id, event_id)  

