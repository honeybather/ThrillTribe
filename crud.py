"""CRUD operations"""

from model import db, User, Category, Activity, Event, EventParticipant, BucketList, ExpertAdvice, connect_to_db
from flask import render_template
import crud

def get_activities():
    """Return all activities"""
    return Activity.query.all()

def get_activity_by_id(activity_id):
    """Return activity id"""
    return  Activity.query.get(activity_id)

def get_user_by_email(email):
    """Return a user by email"""
    # Look for a user in the User table whose email matches the given email.
    # filter adds this condition to the query.
    # User.email == email checks if the email field matches the given email.
    # .first() gets the first matching user or returns None if no match is found.
    return User.query.filter(User.email == email).first()

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user 

def get_events():
    """Return all events."""
    return Event.query.all()

def create_event(activity_id, title, description, date_time, location, skill_level_requirement, cost):
    """Create and return an event."""
    event = Event(activity_id=activity_id, 
                  title=title, 
                  description=description,
                  date_time=date_time, 
                  location=location, 
                  skill_level_requirement=skill_level_requirement, 
                  cost=cost)
    return event

def get_events_by_activity(activity_id):
    """Return events filtered by activity ID."""
    # Filter events where the activity_id matches the given activity_id
    # Event.activity_id == activity_id checks if the activity_id field matches the provided ID
    # .all() gets the all matching event or returns None if no match is found
    return Event.query.filter(Event.activity_id == activity_id).all()

def get_events_by_date(date):
    """Return events filtered by date."""
    # filter events where the date matches the given date
    # event.date == date checks if the data field matches the provided data
    # .all() retireves all events that match the condition 
    return Event.query.filter(Event.date_time == date).all()

def get_event_by_activity_and_date(activity_id, date):
    """Return events filtered by activity_id and date."""
    return Event.query.filter_by(activity_id=activity_id, date=date).all()





def add_user_to_event(user_id, event_id):
    """ Add user to event participants"""
    
    # Retrieve the event and user from the database
    event = get_event_by_id(event_id)
    user = get_user_by_id(user_id)
    
    if event and user:
        # Check if the user is already participating in the event
        existing_participation = EventParticipant.query.filter_by(user_id=user_id, event_id=event_id).first()
        if not existing_participation:
            # Add the user to the event's participants
            new_participation = EventParticipant(user_id=user_id, event_id=event_id, status='Joined', dates_created=datetime.now())
            db.session.add(new_participation)
            db.session.commit()
            return True
    return False

def get_event_participants(event_id):
    """Return all participants for a specific event"""
    return EventParticipant.query.filter_by(event_id=event_id).all()
    
def is_user_participating(user_id, event_id):
    """Check if the user is already participating in the event"""
    return EventParticipant.query.filter_by(user_id=user_id, event_id=event_id).first() is not None

def get_event_by_id(event_id):
    """Return a specific event by its ID."""
    return Event.query.get(event_id)

def create_event_participation(participation_id, event_id, user_id, status, dates_created):
    """Create a new event participation record."""
    new_participation = EventParticipant(
        participation_id=participation_id,
        event_id=event_id,
        user_id=user_id,
        status=status,
        dates_created=dates_created
    )
    db.session.add(new_participation)
    db.session.commit()

def get_events_by_user(user_id):
    """"Return events created by a specific user"""
    return Event.query.filter(Event.user_id == user_id).all()

def add_user_to_event(user_id, event_id):
    """Add user to event participants"""
    event = get_event_by_id(event_id)
    user = get_user_by_id(user_id)
    if event and user:
        event.participants.append(user)
        db.session.commit()
        return True
    return False

if __name__ == '__main__':
    from server import app
    connect_to_db(app)