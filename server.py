"""Server for ThrillTribe app."""

# Import necessary modules and functions from Flask and other files
from flask import (Flask, render_template, request, flash, session, redirect) 
from model import connect_to_db, db 
from jinja2 import StrictUndefined 
import crud # for interacting with the database
from datetime import datetime



app = Flask(__name__) # Create an instance of Flask with the name of the module
app.app_context().push() # Push the application context to be able to use Flask extensions outside of request handlers

app.secret_key = "Rita" # for session management 
app.jinja_env.undefined = StrictUndefined  
# Ensure undefined variables in Jinja templates trigger errors (helps debugging)

@app.route('/')
def homepage():
    """View our first ever homepage!"""
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
    return render_template("activity_details.html", activity=details)
# variable in the template, second is that variable defined 

@app.route("/users")
def list_users():
    """View all users"""
    users = crud.get_users()
    return render_template("user_list.html", users=users)

@app.route("/users/<user_id>")
def show_user(user_id):
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

@app.route("/join_event/<event_id>", methods=["POST"])
def join_event(event_id):
    """Join events"""
# finish this

@app.route("/create_event")
def show_event_form():
    """Show create event form"""
    activities = crud.get_activities()
    return render_template('event_form.html', activities=activities)

@app.route("/create_event", methods=["POST"]) # POST: Used for submitting data to be processed to the server.
def create_event():
    """Create a new event"""
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
    return redirect("/")

@app.route("/events", methods=["GET"]) #GET: Used for retrieving data from the server. 
def all_events():
    """View all events"""
    activities = crud.get_activities() # fetch all activities for filter dropdown
    events = crud.get_events() # fetch all events from the database
    return render_template("all_events.html", activities=activities, events=events)

@app.route("/filter_events")
def filter_events():
    """Display Filtered Events"""

# do it


if __name__ == "__main__":
    connect_to_db(app) # Connect to the database using the app instance
    app.run(host="0.0.0.0", debug=True, port=6060)
    # Run the Flask application on the specified host, enable debugging, and set the port number