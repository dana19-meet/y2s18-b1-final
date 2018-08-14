# Flask-related imports
from flask import Flask, render_template, url_for, redirect, request
from flask import session as login_session
import os
# Add functions you need from databases.py to the next line!
from database import *
import datetime
# Starting the flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)

# App routing code here
@app.route('/', methods=['POST','GET'])
def home():
	if request.method=='POST':
		donor = query_donors_by_email(request.form['email'])
		if donor != None and donor.password==request.form['password']:
			login_session['donor_name'] = donor.name
			login_session['email'] = donor.email
			return render_template('feed_for_recievers.html', donates=query_all_donates(), donor = query_donors_by_email(request.form['email']))
		return redirect('/')

	elif request.method=='GET':
		return render_template('home.html')

		#logout
		# del login_session['donor_name']
		# del login_session['email']    
	
@app.route('/signup_donor', methods=['GET', 'POST'])
def donor():
	if request.method=='POST':
		add_donor(request.form['donor_name'],
			request.form['email'],
			request.form['password'],
			request.form['area'],
			request.form['address'],
			request.form['telephone'])
		donemail=request.form['email']
		donor=query_donors_by_email(donemail)
		return render_template('feed_for_recievers.html', donates=query_all_donates(), donor=donor)
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
		recemail=request.form['email']
		reciever=query_recievers_by_email(recemail)
		return render_template('real_feed_recievers.html', donates=query_all_donates(), reciever=reciever)
	if request.method=='GET':
		return render_template('signup_reciever.html')

@app.route('/donation/<int:donation_id>')
def donation(donation_id):
	donation_1 = query_by_id(donation_id)
	donor_id = donation_1.donor_id
	return render_template('donation.html', 
		donation=query_by_id(donation_id))

@app.route('/feed', methods=['GET', 'POST'])
def feed():
	if request.method=='POST':
		exp=datetime.datetime.strptime(request.form['expiration_date'],'%Y-%m-%d').date()
		donor=query_donors_by_email(login_session['email'])
		add_donation(request.form['donation_name'],
			int(request.form['amount']),
			exp, donor)
		return render_template('feed_for_recievers.html', donates=query_all_donates(), donor=donor)
	if request.method=='GET':
		delete_donations_by_exp(datetime.date.today().strftime("%B %d, %Y"))
		return render_template('feed_for_recievers.html', donates=query_all_donates())
# @app.route('/donation/<int:student_id>')
# def display_student(student_id):
#     return render_template('student.html', student_id=student_id)

# Running the Flask app
if __name__ == "__main__":
	app.run(debug=True)
