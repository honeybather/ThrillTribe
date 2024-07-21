"""Server for ThrillTribe app."""

from flask import (Flask, render_template, request, flash, session, redirect, jsonify) 
from model import connect_to_db, db 
from jinja2 import StrictUndefined 
import crud # for interacting with the database
from datetime import datetime

# import pdb; pdb.set_trace() # learn how to use breakpoints 

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

    # Retrieve email and password from the form submitted by the user
    email = request.form.get('email')
    password = request.form.get('password')

    if email: 
        user = crud.get_user_by_email(email)

        if user:
            flash('Account already created')
            return redirect("/")

        else:
            new_user = crud.create_user(email, password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created')

        return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    """Log in a user"""

    email = request.form.get('email')
    password = request.form.get('password')

    # Retrieve user from the database based on email
    user = crud.get_user_by_email(email)

    if not user or user.password != password:
        flash('Incorrect email or password')
        return redirect("/")
    
    # Store user_id in the session for future requests
    session['user_id'] = user.user_id  
    flash('Logged in')
    return redirect("/")

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
    return render_template('event_form.html', activities=activities)

@app.route("/create_event", methods=["POST"]) 
def create_event():
    """Create a new event"""
    user_id = session.get('user_id')

    if not user_id:
        flash('Please log in to create an event')
        return redirect('/')

    #input for description, date/time, location, skill level, cost
    activity_id = int(request.form.get('activities'))
    title = request.form.get('title')
    description = request.form.get('description')
    location = request.form.get('location')
    skill_level = request.form.get('skill_level')
    cost = float(request.form.get('cost'))
    date = request.form.get('date') 

    format = '%Y-%m-%dT%H:%M'
    date_time = datetime.strptime(date, format) 
    
    event = crud.create_event(activity_id, title, description, date_time, location, skill_level, cost)
    db.session.add(event)
    db.session.commit()
    
    flash('Event created successfuly!')
    return redirect("/events")

@app.route("/join_event/<event_id>", methods=["POST"])
def join_event(event_id):
    """ Join an event """
    
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({"success": False, "message": "Log in to join events"})

    if add_user_to_event(user_id, event_id):
        return jsonify({"success": True, "message": "Successfully joined the event!"})

    else:
        return jsonify({"success": False, "message": "User is already participating or event not found"})

@app.route("/filter_events", methods=["POST"])
def filter_events():
    """Display Filtered Events"""

    # Get parameters from the JSON data
    activity_id = request.json.get('activity_id')
    date = request.json.get('date')

    # Filter events based on provided parameters
    if activity_id and date:
        events = crud.get_events_by_activity_and_date(activity_id, date)
    elif activity_id:
        events = crud.get_events_by_activity(activity_id)
    elif date:
        events = crud.get_events_by_date(date)
    else:
        events = crud.get_events()

    # Convert events to dictionaries
    events_list = [event.to_dict() for event in events]

    return jsonify(events_list)


if __name__ == "__main__":
    connect_to_db(app) # Connect to the database using the app instance
    app.run(host="0.0.0.0", debug=True, port=6060)
    # Run the Flask application on the specified host, enable debugging, and set the port number