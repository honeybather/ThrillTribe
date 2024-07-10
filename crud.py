"""CRUD operations"""

from model import db, User, Category, Activity, Event, BucketList, ExpertAdvice, connect_to_db

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user 

#user1 = User(email='hello@world.com')
#user2 = User(password='test')

def create_category(desctiption):
    """Create and return a category"""

    category = Category(desctiption=desctiption)

    return category 

#new_category = create_category(desctiption='Outdoor Adventures')
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

# new_event = create_event(activity_id=new_activity.activity_id, title='Surfing in Hawaï', 
# description='Let's enjoy surfing the beautiful beaches of Hawaï.',
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
# expert_bio='Drake, Surfing Enthusiast'

if __name__ == '__main__':
    from server import app
    connect_to_db(app)