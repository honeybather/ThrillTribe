"""CRUD operations"""

from model import db, User, Category, Activity, Event, BucketList, ExpertAdvice, connect_to_db
from flask import render_template
import crud

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user 

#user1 = User(email='hello@world.com')
#user2 = User(password='test')

def create_category(description):
    """Create and return a category"""

    category = Category(description=description)

    return category 

#new_category = create_category(description='Outdoor Adventures')
#new_category = create_category('Outdoor Adventures')

def create_activity(name, overview, category_id, season):
    """Create and return a activity"""

    activity = Activity(name=name,
                        overview=overview,
                        category_id=category_id,
                        season=season)
    return activity

#new_activity = create_activity(name='Surfing', overview='Ride the waves', 
# category_id=new_category.category_id, season='Summer')

def get_activities():
    """Return all activities"""
    return Activity.query.all()

def get_activity_by_id(activity_id):
    """Return activity id"""
    return  Activity.query.get(activity_id)

def get_users():
    """Return all users"""
    return User.query.all()

def get_user_by_id(user_id):
    """Return user id"""
    return User.query.get(user_id)

def get_user_by_email(email):
    """Return a user by email"""
    # Look for a user in the User table whose email matches the given email.
    # filter adds this condition to the query.
    # User.email == email checks if the email field matches the given email.
    # .first() gets the first matching user or returns None if no match is found.
    return User.query.filter(User.email == email).first()

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

# from datetime import datetime
# new_event = create_event(activity_id=new_activity.activity_id, title='Surfing in Hawaï', 
# description='Lets enjoy surfing the beautiful beaches of Hawaï.',
# date_time=datetime(2024, 7, 15, 10, 0), location='Malibu Beach', skill_level_requirement='Intermediate', 
# cost=50.0)

def create_bucket_list(activity_id, user_id, status):
    """Create and return a bucket list item."""
    bucket_list_item = BucketList(activity_id=activity_id, 
                                  user_id=user_id, 
                                  status=status)
    return bucket_list_item

#new_bucket_list_item = create_bucket_list(activity_id=new_activity.activity_id,
# user_id=new_user.user_id, status="Pending")
    
def create_expert_advice(activity_id, title, content, expert_bio):
    """Create and return expert advice."""
    expert_advice = ExpertAdvice(activity_id=activity_id, 
                                 title=title, 
                                 content=content, 
                                 expert_bio=expert_bio)
    return expert_advice

# new_expert_advice = create_expert_advice(activity_id=new_activity.activity_id,
# title='Surfing Tips', content='Learn how to catch the perfect wave.',
# expert_bio='Drake, Surfing Enthusiast')

if __name__ == '__main__':
    from server import app
    connect_to_db(app)