from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuring SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'some_secret_key'  # Needed for session management
db = SQLAlchemy(app)

# Model for storing all user data
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    activities = db.Column(db.String(500), nullable=True)  # Allow NULL values
    interests = db.Column(db.String(500), nullable=True)
    favorite_spots = db.Column(db.String(500), nullable=True)

# Home route to display the profile creation screen
@app.route('/')
def home():
    return render_template('profile.html')

# Route to display the location selection screen after submitting the profile
@app.route('/location', methods=['POST'])
def location():
    if request.method == 'POST':
        # Save the basic profile info in session or pass it to the next route
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        session['name'] = name
        session['email'] = email
        session['phone'] = phone
        return render_template('location.html')

# Route to handle future location selection screen

@app.route('/future-location', methods=['POST'])
def future_location():
    
    location = request.form.get('location')  # Get the location from the form

    # Check if the location field is empty
    if not location:
        # If the location is not provided, re-render the form with an error message
        error_message = "Location is required. Please select a location to proceed."
        return render_template('location.html', error=error_message)

   # Save the future location in the session
   # session['future_location'] = location

    # Proceed to the activities page
    # return render_template('activities')

    # Store the user ID in the session to track the user
    # session['user_id'] = new_user.id

    return render_template('future_location.html')

# Route to handle the activities selection page after picking a future location
@app.route('/activities', methods=['POST'])
def activities():
    future_location = request.form.get('future_location')

    # Check if the future location field is empty
    if not future_location:
        error_message = "Future location is required. Please select a location to proceed."
        return render_template('future_location.html', error=error_message)

    # Save the future location in the session
    session['future_location'] = future_location

    # Proceed to activities page
    return render_template('activities.html', future_location=future_location)



# Route for selecting user interests
@app.route('/interests', methods=['POST'])
def interests():
    activities = request.form.getlist('activities')  # Get all selected interests

    if not activities:
        error_message = "Please select at least one activity to proceed."
        return render_template('activities.html', error=error_message)

    # Save interests in session
    session['activities'] = ','.join(activities)

    # Proceed to the favorites page
    return render_template('interests.html', interests=interests)
# Route for sharing favorite spots

@app.route('/favorites', methods=['POST'])
def favorites():
    interests = request.form.getlist('interests')  # Get all selected interests

    if not interests:
        error_message = "Please select at least one interest to proceed."
        return render_template('interests.html', error=error_message)

    # Save interests in session
    session['interests'] = ','.join(interests)

    return render_template('favorites.html', interests=interests)
   


@app.route('/complete', methods=['POST'])
def complete():
    favorite_spots = request.form.getlist('favorites')  # Get all selected favorite spots

    if not favorite_spots:
        error_message = "Please select at least one favorite spot to proceed."
        return render_template('favorites.html', error=error_message)

    # Assuming name, email, phone, location, etc., are stored in the session or provided in the form
    name = session.get('name') 
    email = session.get('email') 
    phone = session.get('phone') 
    location = session.get('location') or request.form['location']
    activities = session.get('activities')  # Use default empty string if not provided
    interests = session.get('interests')  # Use default empty string if not provided

    # Save favorite spots in session
    session['favorite_spots'] = ','.join(favorite_spots)

    # Save data to the database
    new_user = User(
        name=name,
        email=email,
        phone=phone,
        location=location,
        activities=activities,
        interests=interests,
        favorite_spots=session['favorite_spots']
    )
    db.session.add(new_user)
    db.session.commit()

    return "Thank you! Your profile has been created. Now explore the app"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create the SQLite database and table(s)
    app.run(debug=True)