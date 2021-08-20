"""CRUD operations."""

from model import db, User, Location, Plan, Image, Event, Theme, PlanEvent, connect_to_db


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def get_users():
    """Get all users from database."""    

    return User.query.all()


def create_location(zipcode, cityname, countryname):
    """Create and return a new location."""

    location = Location(zipcode=zipcode, cityname=cityname, countryname=countryname)

    db.session.add(location)
    db.session.commit()

    return location

def get_locations():
    """Get all location and details from database."""    

    return Location.query.all()   


def create_plan(user_id=None,location_id=None):
    """Create and return a new plan."""

    plan = Plan(user_id=user_id,location_id=location_id)

    db.session.add(plan)
    db.session.commit()

    return plan  

def get_plans(user_id=None):
    """Create and return a specific user's plan(s)."""
    """If parameter left empty, return first 7 plans"""

    if user_id == None:
        return Plan.query.all()[:7]

    return Plan.query.filter_by(user_id=user_id).all()


def create_image(image_location=None, event_id=None):
    """Create and return a new image."""

    image = Image(image_location=image_location, event_id=event_id)

    db.session.add(image)
    db.session.commit()

    return image    

def get_images(num=None):
    """Get all or a number of images from database."""    

    if num == None:
        return Image.query.all()  
              
    return Image.query.all()[:num]


def create_event(location_id, overview=None, datetime=None):
    """Create and return a new event."""

    event = Event(location_id=location_id, overview=overview, datetime=datetime)
    # EX: >>>event5 = create_event(1,'Movie Night','2020,1,1')

    db.session.add(event)
    db.session.commit()

    return event

def get_events():
    """Get all events and their overview from database."""    

    return Event.query.all()      


def create_theme(tag=None, overview=None):
    """Create and return a new theme."""

    theme = Theme(tag=tag, overview=overview)

    db.session.add(theme)
    db.session.commit()

    return theme     


def add_plan_events(plan_id, event_id):
    """Add event(s) to an existing plan"""

    plan_event = PlanEvent(plan_id=plan_id, event_id=event_id)

    db.session.add(plan_event)
    db.session.commit()

    return plan_event



if __name__ == '__main__':
    from server import app
    connect_to_db(app)