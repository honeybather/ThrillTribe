"""Script to seed database."""

# os: module for interacting with the operating system.
# json: loads data from 'data/movies.json'.
# choice, randint from random: choice picks a random element from a list,
# randint generates a random integer within a specified range for fake users and ratings.
# datetime from datetime: used datetime.strptime to convert a string to a datetime object.
# crud, model, server: files I made.

import os
import json
from random import choice, randint
from datetime import datetime

import crud
from model import connect_to_db, db
from server import app

os.system('dropdb activities')
os.system('createdb activities')

connect_to_db(app)
app.app_context().push()
db.create_all()

# Load data from JSON files
with open('category.json') as f:
    category_data = json.loads(f.read())

# Create Category instances and store them in a list
category_in_db = []
for category in category_data:
    description = (category["description"])
    db_category = crud.create_category(description)
    category_in_db.append(db_category)

db.session.add_all(category_in_db)
db.session.commit()
    

with open('activities.json') as f:
    activity_data = json.loads(f.read())
print(activity_data)

# Create activity instances and store them in a list
activity_in_db = []
for activity in activity_data:
    print(activity)
    description =  (
        activity["name"],
        activity["overview"],
        activity["categoryID"],
        activity["season"]
    )
    db_activity = crud.create_activity(activity["name"], activity["overview"], activity["categoryID"], activity["season"]) 
    activity_in_db.append(db_activity)
#activity = Activity.query.filter(Activity.name == 'MTB').first()
db.session.add_all(activity_in_db)
db.session.commit()


# Generate 10 users; each user will be associated with activities/events
for n in range(10):
    email = f"user{n}@test.com"  
    password = "test"

    user = crud.create_user(email, password)
    db.session.add(user)

    # Assign the user to random activities
    for i in range(10):
        random_activity = choice(activity_data)
        # Assuming you have a function to assign activities to users
        user_activity = crud.create_user_activity(user, random_activity['name'])
        db.session.add(user_activity)

db.session.commit() 
