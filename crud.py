"""CRUD operations"""

from model import db, User, Category, Activity, Event, EventParticipant, BucketList, ExpertAdvice, connect_to_db
from flask import render_template

def create_activity(name, overview, category_id, season):

    activity = Activity(name=name, overview=overview, category_id=category_id, season=season)

    return activity 

def get_activities():
    """Return all activities"""
    return Activity.query.all()

def create_category(description):
    """"return a new category object """
    category = Category(description=description)

    return category 
    
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

def create_event(activity_id, title, description, date_time, location, skill_level_requirement, cost, user_id=None): 
    """Create and return an event."""
    event = Event(activity_id=activity_id, 
                  title=title, 
                  description=description,
                  date_time=date_time, 
                  location=location, 
                  skill_level_requirement=skill_level_requirement, 
                  cost=cost,
                  user_id=user_id
                  )
    return event

def get_events_by_activity(activity_id):
    """Return events filtered by activity ID."""
    # Filter events where the activity_id matches the given activity_id
    # Event.activity_id == activity_id checks if the activity_id field matches the provided ID
    # .all() gets the all matching event or returns None if no match is found
    return Event.query.filter(Event.activity_id == activity_id).all()

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

def get_event_by_id(event_id):
    """Return a specific event by its ID."""

    return Event.query.get(event_id)
    
def is_user_participating(user_id, event_id):
    """Check if the user is already participating in the event"""
    return EventParticipant.query.filter_by(user_id=user_id, event_id=event_id).first() 

def create_event_participation(event_id, user_id):
    """Create a new event participation record."""
    print("Event id", event_id, type(event_id), "User id", user_id, type(user_id))
    print("User", User.query.get(user_id))
    print("Event", Event.query.get(event_id))
    new_participation = EventParticipant(
        event_id=event_id,
        user_id=user_id)
        #status=status,
        #dates_created=dates_created
    
    db.session.add(new_participation)
    db.session.commit()
    return new_participation

def get_user_by_id(user_id):
    """Return user by their ID."""
    return User.query.get(user_id)

def get_events_by_user(user_id):
    """"Return events created by a specific user"""
    return Event.query.filter(Event.user_id == user_id).all()

def get_event_participants(user_id):
    """"Return all events a specific user is participating in"""
    return EventParticipant.query.filter_by(user_id=user_id).all()

def get_bucket_list_items(user_id):
    """"Return all bucket list items for user"""
    return BucketList.query.filter(BucketList.user_id == user_id).all()

def add_bucket_list_item(user_id, activity_id):
    """Add a bucket list item for a user"""
    new_bucket_list_item = BucketList(user_id=user_id, activity_id=activity_id, status='pending')
    db.session.add(new_bucket_list_item)
    db.session.commit()
    return new_bucket_list_item

def get_bucket_list_items(user_id):
    """Return all bucket list items for a user"""
    return BucketList.query.filter(BucketList.user_id==user_id).all()

def mark_bucket_list_item_completed(bucket_list_id):
    """Mark a bucket list item as completed"""
    
    bucket_list_item = BucketList.query.get(bucket_list_id)
    if bucket_list_item:
        bucket_list_item.status = 'completed'
        #db.session.add(bucket_list_item) 
        db.session.commit()
        return bucket_list_item
    return None 

def delete_bucket_list_item(bucket_list_id):
    """Delete a bucket list item"""
    bucket_list_item = BucketList.query.get(bucket_list_id)
    if bucket_list_item:
        db.session.delete(bucket_list_item)
        db.session.commit()
        return bucket_list_item
    return None

if __name__ == '__main__':
    from server import app
    connect_to_db(app)