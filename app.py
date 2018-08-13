# Flask-related imports
from flask import Flask, render_template, url_for, redirect, request, session

# Add functions you need from databases.py to the next line!
from database import *

# Starting the flask app
app = Flask(__name__)

# App routing code here
@app.route('/')
def home():
    return render_template('home.html',donates=query_all())

@app.route('/signup_donor')
def donor():
	if request.method=='POST':
		add_donor(request.form['donor_name'],
			request.form['email'],
			request.form['password'],
			request.form['area'],
			request.form['address'],
			request.form['telephone'])
		return render_template('feed_for_recievers.html')
	if request.method=='GET':
		return render_template('signup_donor.html')

@app.route('/signup_reciever')
def reciever():
	return render_template('signup_reciever.html')

@app.route('/feed')
def feed():
	return render_template('feed_for_recievers.html')
# @app.route('/donation/<int:student_id>')
# def display_student(student_id):
#     return render_template('student.html', student_id=student_id)

# Running the Flask app
if __name__ == "__main__":
    app.run(debug=True)
