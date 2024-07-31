"""Server for ThrillTribe app."""

from flask import (Flask, render_template, request, flash, session, redirect, jsonify, url_for ) 
from model import connect_to_db, db 
from model import db, User, Category, Activity, Event, BucketList, ExpertAdvice
from jinja2 import StrictUndefined 
import crud
from datetime import datetime

app = Flask(__name__) # Create an instance of Flask with the name of the module
app.app_context().push() # Push the application context to be able to use Flask extensions outside of request handlers

app.secret_key = "Rita" # for session management 
app.jinja_env.undefined = StrictUndefined  
# Ensure undefined variables in Jinja templates trigger errors (helps debugging)

@app.route('/')
def homepage():
    """View my first ever homepage!"""
    return render_template('homepage.html')

@app.route("/activities")
def all_activities():
    """View all activities"""
    activities = crud.get_activities()
    return render_template("all_activities.html", activities=activities)

@app.route("/activities/<activity_id>")
def show_activity(activity_id):
    """Show details on a particular activity."""
    details = crud.get_activity_by_id(activity_id)
    return render_template("activity_details.html", activity=details)# variable in the template, second is that variable defined 


    """Show details on a selected user"""
    user = crud.get_user_by_id(user_id)
    return render_template("user_list.html", user=user)

@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user"""

    # Retrieve username, email, and password from the form submitted by the user
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if username already exists
    user = crud.get_user_by_username(username)
    if user:
        flash('Username already exists')
        return redirect("/")

    # Check if email already exists
    user = crud.get_user_by_email(email)
    if user:
        flash('Email already in use')
        return redirect("/")

    new_user = crud.create_user(username, email, password)
    db.session.add(new_user)
    db.session.commit()
    flash('Account created')
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    """Log in a user"""

    username = request.form.get('username')
    password = request.form.get('password')

    # Retrieve user from the database based on username
    user = crud.get_user_by_username(username)

    if not user or user.password != password:
        flash('Incorrect username or password')
        return redirect("/")

    # Store user_id in the session for future requests
    session['user_id'] = user.user_id  
    flash('Logged in')
    return redirect("/")

@app.route("/users/<int:user_id>", methods=["GET"])
def view_profile(user_id):
    """View user profile"""

    #user_id = session.get('user_id')
    user = crud.get_user_by_id(user_id) 
    if not user:
        flash('User not found')
        return redirect('/')

    created_events = crud.get_events_by_user(user_id)
    joined_events = crud.get_event_participants(user_id)
    bucket_list_items = crud.get_bucket_list_items(user_id)
    activities = crud.get_activities()

    print(f"User: {user}") 
    print(f"Created Events: {created_events}")
    print(f"Joined Events: {joined_events}")
    print(f"Bucket List: {bucket_list_items}")
    print(f"Activities: {activities}")


    return render_template(
        "user_profile.html", 
        user=user,
        created_events=created_events,
        joined_events=joined_events,
        bucket_list_items=bucket_list_items,
        activities=activities
        )

@app.route("/events") 
def all_events():
    """View all events created by all users"""

    user_id = session.get('user_id')
    activities = crud.get_activities()  # Fetch all activities for the filter dropdown
    all_events = crud.get_events()  # Fetch all all events

    # Check if user is logged in
    if user_id:
        user = crud.get_user_by_id(user_id)
        if not user:
            flash("User not found")
            return redirect("/")

    return render_template("all_events.html", activities=activities, events=all_events, user_id=user_id)

@app.route("/create_event")
def show_event_form():
    """Show create event form"""
    activities = crud.get_activities()
    print(activities)
    return render_template('event_form.html', activities=activities)

@app.route("/create_event", methods=["POST"]) 
def create_event():
    """Create a new event"""
    user_id = session.get('user_id')

    if not user_id:
        flash('Please log in to create an event')
        return redirect('/')

    activity_id = int(request.form.get('activities'))
    title = request.form.get('title')
    description = request.form.get('description')
    location = request.form.get('location')
    skill_level = request.form.get('skill_level')
    cost = float(request.form.get('cost'))
    date = request.form.get('date') 
    
    format = '%Y-%m-%dT%H:%M'
    date_time = datetime.strptime(date, format) 
    
    event = crud.create_event(activity_id, title, description, date_time, location, skill_level, cost, user_id)
    print(event)

    db.session.add(event)
    db.session.commit()
    
    flash('Event created successfuly!')
    return redirect(url_for('homepage')) 

@app.route("/join_event/<int:event_id>", methods=["POST"])
def join_event(event_id):
    """Join an event"""
    
    user_id = session.get('user_id')

    # Ensure the event exists
    event = crud.get_event_by_id(event_id)

    if not event:
        flash('Event not found.')
        return redirect('/events')

    # Check if the user is already participating
    existing_participation = crud.is_user_participating(user_id, event_id)

    if existing_participation:
        flash('You are already participating in this event.')
        return redirect('/events')

    # Add user to the event
    print("User id", user_id, type(user_id))
    participation = crud.create_event_participation(event_id=event_id, user_id=user_id)
    print("Event Participation", participation)
    db.session.add(participation)
    db.session.commit() 
    flash('Successfully joined the event!')
    
    return redirect('/events')

@app.route("/filter_events", methods=["POST"])
def filter_events():
    """Display Filtered Events"""

    # Get parameters from the JSON data
    activity_id = request.json.get('activity_id')

    # Filter events based on activity_id
    if activity_id:
        events = crud.get_events_by_activity(activity_id)
    else:
        events = crud.get_events()
    print(events)

    events_list = []

    for event in events:
        # the key in the dictionary is what is read by javascript,
        # the value in the dictionary is the column in the events table
        filtered_event = {
            'name': event.title,
            'description': event.description,
            'date': event.date_time  
        }
        events_list.append(filtered_event)
    return jsonify(events_list)

@app.route("/bucket_list/add", methods=["POST"])
def add_bucket_list():
    """Add an item to the bucket list"""

    user_id = session.get('user_id') 

    activity_id = int(request.form.get('activity_id'))
    crud.add_bucket_list_item(user_id, activity_id)
    flash('Bucket list item added!')
    return redirect(f"/users/{user_id}")

@app.route("/bucket_list/complete/<int:bucket_list_id>", methods=["POST"])
def complete_bucket_list_item(bucket_list_id):
    """Mark a bucket list item as completed"""

    user_id = session.get('user_id')  

    crud.mark_bucket_list_item_completed(bucket_list_id)
    flash('Bucket list item completed!')
    return redirect(f"/users/{user_id}")

@app.route("/bucket_list/delete/<int:bucket_list_id>", methods=["POST"])
def delete_bucket_list_item(bucket_list_id):
    """Delete a bucket list item"""

    user_id = session.get('user_id') 

    crud.delete_bucket_list_item(bucket_list_id)
    flash('Bucket list item deleted.')
    return redirect(f"/users/{user_id}")

@app.route('/bucket_list/undo/<int:bucket_list_id>', methods=['POST'])
def undo_bucket_list_completion(bucket_list_id):
    bucket_list_item = BucketList.query.get(bucket_list_id)
    if bucket_list_item:
        bucket_list_item.status = 'pending'
        db.session.commit()
    return redirect(url_for('view_profile', user_id=bucket_list_item.user_id))

@app.route("/events/<int:event_id>")
def show_event(event_id):
    """Show details for a specific event."""
    event = crud.get_event_by_id(event_id)
    participants = crud.get_event_participants(event_id)
    
    return render_template("event_details.html", event=event, participants=participants)

if __name__ == "__main__":
    connect_to_db(app) # Connect to the database using the app instance
    app.run(host="0.0.0.0", debug=True, port=6060)
    # Run the Flask application on the specified host, enable debugging, and set the port number