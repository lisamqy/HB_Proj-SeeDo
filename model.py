from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A User."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(16), nullable=False)
    
    plans = db.relationship("Plan", backref="users") 
    # EX: user1.plans to get all plans related to user1; plan1.user to find user who created plan1

    def __repr__(self):
        """Show user's id and email."""
        return f"<User user_id={self.user_id} email={self.email}>"


class Location(db.Model):
    """A Location."""

    __tablename__ = "locations"

    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    zipcode = db.Column(db.Integer)
    cityname = db.Column(db.String(20),nullable=False)
    statename = db.Column(db.String(20))

    events = db.relationship("Event", backref="locations") 
    # EX: loc1.events to get all events related to loc1, event1.location to find location details

    def __repr__(self):
        """Show location details."""
        return f"<Location location_id={self.location_id} cityname={self.cityname} zipcode={self.zipcode}>"


class Plan(db.Model):
    """Plan created by User"""        

    __tablename__ = "plans"

    plan_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"),
                        nullable=False)
    location_id = db.Column(db.Integer,
                            db.ForeignKey("locations.location_id"),
                            nullable=False)  
    overview = db.Column(db.String(100))                            

    events = db.relationship("Event",
                             secondary="planevent",
                             backref="plans")                                                 
    
    def __repr__(self):
        """Show plan details."""
        return f"<Plan plan_id={self.plan_id} user_id={self.user_id} location={self.location_id}>"                                            


class PlanEvent(db.Model):
    """An association for Plan and Event"""

    __tablename__ = "planevent"

    planevent_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plan_id = db.Column(db.Integer,
                        db.ForeignKey("plans.plan_id"),
                        nullable=False)
    event_id = db.Column(db.Integer,
                            db.ForeignKey("events.event_id"),
                            nullable=False)
    

class Event(db.Model):
    """An Event."""

    __tablename__ = "events"

    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location_id = db.Column(db.Integer,
                            db.ForeignKey("locations.location_id"),
                            nullable=False)
    overview = db.Column(db.String(100), nullable=False)
    datetime = db.Column(db.DateTime)
    liked = db.Column(db.Integer)

    images = db.relationship("Image", backref="events") 
    # EX: event1.images to get all images related to event1, img1.event to find which event img from

    themes = db.relationship("Theme",
                             secondary="eventthemes",
                             backref="events")

    def __repr__(self):
        """Show event details."""
        return f"<Event event_id={self.event_id} overview={self.overview}>"                          
    

class EventTheme(db.Model):
    """Theme of a specific event."""

    __tablename__ = "eventthemes" 

    event_theme_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer,
                        db.ForeignKey('events.event_id'),
                        nullable=False)
    theme_id = db.Column(db.Integer,
                         db.ForeignKey('themes.theme_id'),
                         nullable=False)    


class Theme(db.Model):
    """A Theme/Tag to describe events"""

    __tablename__ = "themes"

    theme_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag = db.Column(db.String, nullable=False, unique=True)
    overview = db.Column(db.String(100))  

    def __repr__(self):
        """Show theme details."""
        return f"<Theme theme_id={self.theme_id} tag={self.tag}>"

 
class Image(db.Model):
    """An image."""

    __tablename__ = "images" 

    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_location = db.Column(db.String)
    event_id = db.Column(db.Integer,
                        db.ForeignKey("events.event_id"))

    def __repr__(self):
        """Show image details."""
        return f"<Image image_id={self.image_id} Related to event.id={self.event_id}>"                        


def connect_to_db(app, db_uri="postgresql:///project"):
    """Connect to database."""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)



if __name__ == '__main__':
    from server import app

    connect_to_db(app)
    print("Connected to DB.")
