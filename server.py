"""Server for ThrillTribe app."""

# Import necessary modules and functions from Flask and other files
from flask import (Flask, render_template, request, flash, session, redirect) 
from model import connect_to_db, db 
from jinja2 import StrictUndefined 
import crud # for interacting with the database


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

@app.route("/users", method=["POST"])
def register_user():
    """Create a new user"""
# do it


if __name__ == "__main__":
    connect_to_db(app) # Connect to the database using the app instance
    app.run(host="0.0.0.0", debug=True, port=6060)
    # Run the Flask application on the specified host, enable debugging, and set the port number