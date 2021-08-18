from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A User."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(16), nullable=False)
    

    def __repr__(self):
        """Show user's id and email."""
        return f"<User user_id={self.user_id} email={self.email}>"


class Location(db.Model):
    """A Location."""

    __tablename__ = "locations"

    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    zipcode = db.Column(db.Integer)
    cityname = db.Column(db.String(20),nullable=False)
    countryname = db.Column(db.String(20))
    plan_id = db.Column(db.Integer,
                        db.ForeignKey("plans.plan_id"))

    plan = db.relationship("Plan", backref="locations")

    def __repr__(self):
        """Show location details."""
        return f"<Location location_id={self.location_id} cityname={self.cityname} zipcode={self.zipcode}>"


class Plan(db.Model):
    """Plan created by User"""        

    __tablename__ = "plans"

    plan_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # location_id = db.Column(db.Integer,
    #                         db.ForeignKey("locations.location_id"),
    #                         nullable=False)
    # event_id = db.Column(db.Integer,
    #                      db.ForeignKey("events.event_id"),
    #                      nullable=False)
    # image_id = db.Column(db.Integer,
    #                      db.ForeignKey("images.image_id"))   
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"))

    user = db.relationship("User", backref="plans")   
 

class Image(db.Model):
    """An image."""

    __tablename__ = "images" 

    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_location = db.Column(db.String)
    plan_id = db.Column(db.Integer,
                        db.ForeignKey("plans.plan_id"))

    plan = db.relationship("Plan", backref="images")                                           


class Event(db.Model):
    """An Event."""

    __tablename__ = "events"

    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location_id = db.Column(db.Integer,
                            db.ForeignKey("locations.location_id"),
                            nullable=False)
    overview = db.Column(db.String(100))
    datetime = db.Column(db.DateTime)
    themes = db.relationship("Theme", 
                            secondary= "event_themes",
                            backref="events")

    plan_id = db.Column(db.Integer,
                        db.ForeignKey("plans.plan_id"))

    plan = db.relationship("Plan", backref="events")                            
    

class EventTheme(db.Model):
    """Theme of a specific event."""

    __tablename__ = "event_themes" 

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
    tag = db.Column(db.String(20), nullable=False)
    overview = db.Column(db.String(100))  



def connect_to_db(app, db_uri="postgresql:///project"):
    """Connect to database."""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()



if __name__ == '__main__':
    from server import app

    connect_to_db(app)
    print("Connected to DB.")
