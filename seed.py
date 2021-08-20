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
for num in range(10):
    email = f"user{num}@email.com"
    password = "123"

    user = crud.create_user(email,password)


# Load location data from JSON file
with open("data/locations.json") as f:
    location_data = json.loads(f.read())
# Create locations
locations_db = []
for location in location_data:
    address, cityname, zipcode = (
        location["address"],
        location["cityname"],
        location["zipcode"]
    )
    countryname = "USA"

    location = crud.create_location(zipcode, cityname, countryname)
    locations_db.append(location)


# Create x events
names = ["Amy", "Betty", "Charles", "Danny", "Ella", "Felicia", "George", "Hailey"]
events = ["birthday party", "pool party", "backyard BBQ", "sleepover", "hikign trip", "picnic trip", "potluck"]

for name in names:
    location_id = randint(1,20)
    x = choice(events)
    overview = f"{name}'s {x}"
    datetime=datetime.now()

    event = crud.create_event(location_id,overview, datetime)


# Create x themes
with open("data/themes.json") as f:
    theme_data = json.loads(f.read())

themes_db = []
for theme in theme_data:
    tag = theme
    overview = f"the theme is related to: {theme}"

    theme = crud.create_theme(tag, overview)
    themes_db.append(theme)
