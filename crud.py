"""CRUD operations."""

from model import db, User, Location, Plan, Image, Event, Theme, connect_to_db


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user


def create_location(zipcode, cityname, countryname,plan_id=None):
    """Create and return a new location."""

    location = Location(zipcode=zipcode, cityname=cityname, countryname=countryname, plan_id=plan_id)

    db.session.add(location)
    db.session.commit()

    return location


def create_plan(user_id=None):
    """Create and return a new plan."""

    plan = Plan(user_id=user_id)

    db.session.add(plan)
    db.session.commit()

    return plan  


def create_image(image_location=None, plan_id=None):
    """Create and return a new image."""

    image = Image(image_location=image_location, plan_id=plan_id)

    db.session.add(image)
    db.session.commit()

    return plan      


def create_event(location_id, overview=None, datetime=None, plan_id=None):
    """Create and return a new event."""

    event = Event(location_id=location_id, overview=overview, datetime=datetime, plan_id=plan_id)

    db.session.add(event)
    db.session.commit()

    return event


def create_theme(tag=None, overview=None):
    """Create and return a new theme."""

    theme = Theme(tag=tag, overview=overview)

    db.session.add(theme)
    db.session.commit()

    return theme     


if __name__ == '__main__':
    from server import app
    connect_to_db(app)