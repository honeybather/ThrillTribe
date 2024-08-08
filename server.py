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
    categories = crud.get_all_categories()
    activities = crud.get_activities()
    return render_template("all_activities.html", categories=categories, activities=activities)

@app.route("/activities/<activity_id>")
def show_activity(activity_id):
    """Show details on a particular activity."""
    # fetch activity details 
    details = crud.get_activity_by_id(activity_id)
    # fetch all events for the activity
    events = crud.get_events_by_activity(activity_id)
    return render_template("activity_details.html", activity=details, events=events)# variable in the template, second is that variable defined 


    """Show details on a selected user"""
    user = crud.get_user_by_id(user_id)
    return render_template("user_list.html", user=user)

@app.route("/signup", methods=["POST"])
def register_user():
    """Create a new user"""

    # Retrieve info from the form submitted by the user
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if username already exists
    if crud.get_user_by_username(username):
        flash("Username already exists", "error")
        return redirect(url_for('signup_page'))

    # Check if email already exists
    if crud.get_user_by_email(email):
        flash("Email already in use", "error")
        return redirect(url_for('signup_page'))

    # Create new user
    crud.create_user(username, email, password)
    db.session.commit()
    flash("Account created successfully", "success")
    return redirect(url_for('login_page'))

@app.route("/login", methods=["POST"])
def login():
    """Log in a user"""

    username = request.form.get('username')
    password = request.form.get('password')

    # retrieve user from the database based on username
    user = crud.get_user_by_username(username)

    if not user or user.password != password:
        flash("Incorrect username or password", "error")
        return redirect(url_for('login_page'))

    # store user_id in the session for future requests
    session['user_id'] = user.user_id
    flash("Logged in successfully", "success")

    return redirect(url_for('view_profile', user_id=user.user_id))

@app.route("/login", methods=["GET"])
def login_page():
    """Render the login page"""
    return render_template('login.html')

@app.route("/signup", methods=["GET"])
def signup_page():
    """Render the sign-up page"""
    return render_template('signup.html')

@app.route("/logout")
def logout():
    """Log out the user and redirect to the login page"""

    session.pop('user_id', None)

    flash("Logged out successfully", "success")
    return redirect(url_for('login_page'))

@app.route("/users/<int:user_id>", methods=["GET"])
def view_profile(user_id):
    """View user profile"""

    user = crud.get_user_by_id(user_id) 
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 401

    created_events = crud.get_events_by_user(user_id)
    joined_events = crud.get_event_participants(user_id) 
    bucket_list_items = crud.get_bucket_list_items(user_id)
    activities = crud.get_activities()

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
            return jsonify({"status": "error", "message": "User not found"}), 401

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
       return jsonify({'success': False, 'message': 'Please log in to create an event'}), 401

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
    
    return redirect(url_for('all_events'))
    #return jsonify({'success': True, 'message': 'Event created successfully!'}), 201

@app.route("/join_event/<int:event_id>", methods=["POST"])
def join_event(event_id):
    """Join an event"""
    
    user_id = session.get('user_id')

    # Ensure the event exists
    event = crud.get_event_by_id(event_id)

    if not event:
        return jsonify({'success': False, 'message': 'Event not found.'}), 404

    # Check if the user is already participating
    existing_participation = crud.is_user_participating(user_id, event_id)

    if existing_participation:
        return jsonify({'success': False, 'message': 'You are already participating in this event.'}), 400

    # Add user to the event
    participation = crud.create_event_participation(event_id=event_id, user_id=user_id)
    db.session.add(participation)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Successfully joined the event!'})

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

@app.route("/filter_activities", methods=["POST"])
def filter_activities():
    """Display Filtered Activities"""

    # Get parameters from the JSON data
    category_id = request.json.get('category_id')
    print('Category ID:', category_id)

    # Filter activities based on category_id
    if category_id:
        activities = crud.get_activities_by_category(category_id)
    else:
        activities = crud.get_activities()

    activities_list = []
    for activity in activities:
        # The key in the dictionary is what is read by JavaScript,
        # the value in the dictionary is the column in the activities table
        filtered_activity = {
            'id': activity.activity_id,
            'name': activity.name,
            'overview': activity.overview, 
        }
        activities_list.append(filtered_activity)

    return jsonify(activities_list)

@app.route("/bucket_list/add", methods=["POST"])
def add_bucket_list():
    """Add an item to the bucket list"""

    user_id = session.get('user_id') 

    activity_id = int(request.form.get('activity_id'))
    crud.add_bucket_list_item(user_id, activity_id)
    return redirect(url_for('view_profile', user_id=user_id))
    #return jsonify({'success': True, 'message': 'Bucket list item added successfully!'}), 201

@app.route("/bucket_list/complete/<int:bucket_list_id>", methods=["POST"])
def complete_bucket_list_item(bucket_list_id):
    """Mark a bucket list item as completed"""

    user_id = session.get('user_id')  

    crud.mark_bucket_list_item_completed(bucket_list_id)
    return redirect(url_for('view_profile', user_id=user_id))
    #return jsonify({'success': True, 'message': 'Bucket list item completed!'}), 201

@app.route("/bucket_list/delete/<int:bucket_list_id>", methods=["POST"])
def delete_bucket_list_item(bucket_list_id):
    """Delete a bucket list item"""

    user_id = session.get('user_id') 

    crud.delete_bucket_list_item(bucket_list_id)
    return redirect(url_for('view_profile', user_id=user_id))
    #return jsonify({'success': True, 'message': 'Bucket list item deleted.'}), 201

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