"""CRUD operations."""

from model import db, User, Location, Plan, Image, Event, Theme, connect_to_db


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


def create_plan(user_id=None,location_id=None):
    """Create and return a new plan."""

    plan = Plan(user_id=user_id,location_id=location_id)

    db.session.add(plan)
    db.session.commit()

    return plan  


def create_image(image_location=None, event_id=None):
    """Create and return a new image."""

    image = Image(image_location=image_location, event_id=event_id)

    db.session.add(image)
    db.session.commit()

    return image      


def create_event(location_id, overview=None, datetime=None):
    """Create and return a new event."""

    event = Event(location_id=location_id, overview=overview, datetime=datetime)
    # EX: >>>event5 = create_event(1,'Movie Night','2020,1,1')

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