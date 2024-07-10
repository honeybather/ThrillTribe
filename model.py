"""Models for ThrillTribe website."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    # Define relationship to EventParticipant: each user can have multiple participations
    event_participants = db.relationship("EventParticipant", back_populates="user")
    # Define relation to BucketList: each user can have multiple bucketlist items
    bucket_list_items = db.relationship("BucketList", back_populates="user")

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"
    

class Category(db.Model):
     """Activty categories."""

     __tablename__ = "categories"

     category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
     description = db.Column(db.String) 

     activities = db.relationship("Activity", back_populates="category") 

     def __repr__(self):
        return f"<Category category_id={self.category_id} description={self.description}>"

     
     
class Activity(db.Model):
    """An activity."""

    __tablename__ = "activities"
    activity_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, unique=True)
    overview = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id')) 
    season = db.Column(db.String)

    categories = db.relationship("Category", back_populates="activity") 
    events = db.relationship("Event", back_populates="activity") 
    bucket_list = db.relationship("BucketList", back_populates="activity") 
    expert_advice = db.relationship("ExpertAdvice", back_populates="activity") 


    def __repr__(self):
        return f"<Activity activity_id={self.activity_id} name={self.name}>"


class Event(db.Model):
    """An event."""

    __tablename__ = "events"

    event_id = db.Column(db.Integer, autoincrement=True, primary_key=True) 
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.activity_id')) 
    title = db.Column(db.String, nullable=False) 
    description = db.Column(db.String) 
    date_time = db.Column(db.DateTime, nullable=False) 
    location = db.Column(db.String, nullable=False) 
    skill_level_requirement = db.Column(db.String) 
    cost = db.Column(db.Float)

    activity = db.relationship('Activity', backref='event')
    event_participants = db.relationship('EventParticipants', backref='event')

    def __repr__(self):
            return f"<Event event_id={self.event_id} title={self.title}>"
    

class EventParticipant(db.Model):
    """Association table between users and events."""

    __tablename__ = "event_participants"

    participation_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    status = db.Column(db.String)
    dates_created = db.Column(db.DateTime)

    event = db.relationship('Event', backref='participant')
    user = db.relationship('User', backref='participant')

    def __repr__(self):
         return f"<EventParticipant participation_id={self.participation_id}>"
    

class BucketList(db.Model):
    """A bucket list item."""

    __tablename__ = "bucket_list"

    bucket_list_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.activity_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    status = db.Column(db.String)

    user = db.relationship('User', backref = 'bucket_list')
    activity = db.relationship('Activity', backref = 'bucket_list')

    def __repr__(self):
         return f"<BucketList bucket_list_id={self.bucket_list_id}>"
    

class ExpertAdvice(db.Model):
    """Expert advice related to activities."""

    __tablename__ = "expert_advice"

    advice_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.activity_id'))
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    expert_bio = db.Column(db.String)

    activity = db.relationship('Activity', backref = 'expert_advice')

    def __repr__(self):
         return f"<ExpertAdvice advice_id={self.advice_id} title={self.title}>"
    

def connect_to_db(app):
    """Connect the database to Flask app."""

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///activities"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print("Connected to the db!")