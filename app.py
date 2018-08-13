# Flask-related imports
from flask import Flask, render_template, url_for, redirect, request
from flask import session as login_session

# Add functions you need from databases.py to the next line!
from database import *
import datetime
# Starting the flask app
app = Flask(__name__)


# App routing code here
@app.route('/')
def home():
	# donor = query_donors_by_email(request.form['email'])
	# if donor == None:
	# # login
	# 	if donor.password==request.form['password']:
	# 		login_session['donor_name'] = donor.donor_name
	# 		login_session['email'] = donor.email
	# 		return render_template('feed_for_recievers.html')
		#logout
		# del login_session['donor_name']
		# del login_session['email']

    return render_template('home.html',donates=query_all_donates())

@app.route('/signup_donor', methods=['GET', 'POST'])
def donor():
	print(request.method)
	if request.method=='POST':
		print("here")
		add_donor(request.form['donor_name'],
			request.form['email'],
			request.form['password'],
			request.form['area'],
			request.form['address'],
			request.form['telephone'])
		return render_template('feed_for_recievers.html', donates=query_all_donates())
	if request.method=='GET':
		return render_template('signup_donor.html')

@app.route('/signup_reciever', methods=['GET', 'POST'])
def reciever():
	if request.method=='POST':
		add_reciever(request.form['reciever_name'],
			request.form['email'],
			request.form['password'],
			request.form['area'],
			request.form['telephone'])
		return render_template('feed_for_recievers.html', donates=query_all_donates())
	if request.method=='GET':
		return render_template('signup_reciever.html')

@app.route('/feed', methods=['GET', 'POST'])
def feed():
	if request.method=='POST':
		exp=datetime.datetime.strptime(request.form['expiration_date'],'%Y-%m-%d').date()
		add_donation(request.form['donation_name'],
			request.form['amount'],
			exp)
		return render_template('feed_for_recievers.html', donates=query_all_donates())
	if request.method=='GET':
		return render_template('feed_for_recievers.html', donates=query_all_donates())
# @app.route('/donation/<int:student_id>')
# def display_student(student_id):
#     return render_template('student.html', student_id=student_id)

# Running the Flask app
if __name__ == "__main__":
    app.run(debug=True)
