# Flask-related imports
from flask import Flask, render_template, url_for, redirect, request, session

# Add functions you need from databases.py to the next line!
from databases import add_student, get_all_students

# Starting the flask app
app = Flask(__name__)

# App routing code here
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup_donor')
def donor():
	return render_template('signup_donor.html')

@app.route('/signup_reciever')
def reciever():
	return render_template('signup_reciever.html')

# Running the Flask app
if __name__ == "__main__":
    app.run(debug=True)
