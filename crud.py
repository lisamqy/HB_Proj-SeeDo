"""CRUD operations."""

from model import db, User, Location, Plan, PlanEvent, Event, EventTheme, Theme, connect_to_db


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user


def create_location(zipcode, cityname, countryname):
    """Create and return a new location."""

    location = Location(zipcode=zipcode, cityname=cityname, countryname=countryname)

    db.session.add(location)
    db.session.commit()

    return location


def create_event()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)