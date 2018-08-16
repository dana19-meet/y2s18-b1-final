# Flask-related imports
from flask import Flask, render_template, url_for, redirect, request
from flask import session as login_session
import os
# Add functions you need from databases.py to the next line!
from database import *
import datetime
from flask_mail import Mail, Message


# Starting the flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)


app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'foodsecure1@gmail.com'
app.config['MAIL_PASSWORD'] = r'1234%abcd'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


# App routing code here
@app.route('/', methods=['POST','GET'])
def home():
	if request.method=='POST':
		donor = query_donors_by_email(request.form['email'])
		reciever=query_recievers_by_email(request.form['email'])
		if donor != None and donor.password==request.form['password']:
			login_session['donor_name'] = donor.name
			login_session['email'] = donor.email
			return redirect(url_for('home_sign_in'))
		elif reciever != None and reciever.password==request.form['password']:
			login_session['reciever_name'] = reciever.reciever_name
			login_session['email'] = reciever.email
			return redirect(url_for('home_sign_in'))
		return redirect('/')

	elif request.method=='GET':
		return render_template('home.html')
  

@app.route('/home_signed_in', methods=['GET','POST'])
def home_sign_in():
	if request.method=='GET':
		donor=query_donors_by_email(login_session['email'])
		reciever=query_recievers_by_email(login_session['email'])
		if donor != None:
			return render_template('home_logged_in.html', donor=donor)
		if reciever!= None:
			return render_template('home_logged_in.html', reciever=reciever)



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
		msg = Message('Hello', sender = 'foodsecure1@gmail.com', recipients = [request.form['email']])
		msg.body = "Hello! You have been signed up for foodsecure.com as a donor"
		mail.send(msg)
		return redirect(url_for('home'))
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
		msg = Message('Hello', sender = 'foodsecure1@gmail.com', recipients = [request.form['email']])
		msg.body = "Hello! You have been signed up for foodsecure.com as a reciever"
		mail.send(msg)
		return redirect(url_for('home'))
	if request.method=='GET':
		return render_template('signup_reciever.html')

@app.route('/donation/<int:donation_id>')
def donation(donation_id):
	donation_1 = query_by_id(donation_id)
	donor_id = donation_1.donor_id
	return render_template('donation.html', 
		donation=query_by_id(donation_id))

@app.route('/donation_reciever/<int:donation_id>')
def reciever_donation(donation_id):
	donation_1 = query_by_id(donation_id)
	donor_id = donation_1.donor_id
	return render_template('donation_reciever.html', 
		donation=query_by_id(donation_id))

@app.route('/my_donations', methods=['GET', 'POST'])
def account_donor():
	today=datetime.datetime.now().strftime ("%Y-%m-%d")
	delete_donations_by_exp(today)
	if request.method=='POST':  
		exp=datetime.datetime.strptime(request.form['expiration_date'],"%Y-%m-%d").date()
		donor=query_donors_by_email(login_session['email'])
		if donor == None:
			return redirect(url_for('home'))
		today=datetime.datetime.now().strftime ("%Y-%m-%d")
		delete_donations_by_exp(today)
		add_donation(request.form['donation_name'],
			int(request.form['amount']),
			exp, donor)
		mydonations=query_donations_by_donorid(donor.donor_id)
		return render_template('feed_for_recievers.html', mydonations=mydonations, donor=donor)
	if request.method=='GET':
		today=datetime.datetime.now().strftime ("%Y-%m-%d")
		delete_donations_by_exp(today)
		donor=query_donors_by_email(login_session['email'])
		mydonations=query_donations_by_donorid(donor.donor_id)
		return render_template('feed_for_recievers.html', mydonations=mydonations, donor=donor)

@app.route('/donations', methods=['GET', 'POST'])
def feed():
	today=datetime.datetime.now().strftime ("%Y-%m-%d")
	delete_donations_by_exp(today)
	if request.method=='POST':  
		exp=datetime.datetime.strptime(request.form['expiration_date'],"%Y-%m-%d").date()
		donor=query_donors_by_email(login_session['email'])
		if donor == None:
			return redirect(url_for('home'))
		today=datetime.datetime.now().strftime ("%Y-%m-%d")
		delete_donations_by_exp(today)
		add_donation(request.form['donation_name'],
			int(request.form['amount']),
			exp, donor)
		mydonations=query_donations_by_donorid(donor.donor_id)
		return render_template('feed_for_recievers.html', mydonations=mydonations, donor=donor)
	if request.method=='GET':
		today=datetime.datetime.now().strftime ("%Y-%m-%d")
		delete_donations_by_exp(today)
		donor=query_donors_by_email(login_session['email'])
		mydonations=query_donations_by_donorid(donor.donor_id)
		return render_template('all_donations_donor.html', mydonations=mydonations, donor=donor)

@app.route('/my_requests/<int:request_id>', methods=['GET', 'POST'])
def requests(request_id):
	if request.method=='POST':  
		reciever=query_recievers_by_email(login_session['email'])
		if reciever == None:
			return redirect(url_for('home'))
		add_request(request.form['request_name'],
			int(request.form['amount']), reciever)
		myrequests=query_requests_by_recieverid(reciever.reciever_id)
		return render_template('account_reciever.html', myrequests=myrequests, reciever=reciever)
	if request.method=='GET':
		frequest = query_request_by_id(request_id)
		return render_template('request.html', request=frequest, login_session=login_session)
# we were here a 

@app.route('/account_reciever',methods=['POST','GET'])
def account_reciever():
	if request.method=='GET':
		reciever=query_recievers_by_email(login_session['email'])
		myrequests=query_requests_by_recieverid(reciever.reciever_id)
		return render_template('account_reciever.html', reciever=reciever, myrequests=myrequests)
	if request.method=='POST':  
		reciever=query_recievers_by_email(login_session['email'])
		if reciever == None:
			return redirect(url_for('home'))
		add_request(request.form['request_name'],
			int(request.form['amount']), reciever)
		myrequests=query_requests_by_recieverid(reciever.reciever_id)
		return render_template('account_reciever.html', myrequests=myrequests, reciever=reciever)

@app.route('/reciever_feed', methods=['GET'])
def recieverfeed():
	if request.method=='GET':
		today=datetime.datetime.now().strftime ("%Y-%m-%d")
		delete_donations_by_exp(today)
		reciever=query_recievers_by_email(login_session['email'])
		donor=query_donors_by_email(login_session['email'])
		return render_template('real_feed_recievers.html', donates=query_all_donates(),donor=donor, reciever=reciever)

@app.route('/edit_donation/<int:food_id>', methods=['GET','POST'])
def edit_donation(food_id):
	if request.method=='POST':
		exp=datetime.datetime.strptime(request.form['expiration_date'],"%Y-%m-%d").date()
		update_donation(food_id,exp,int(request.form['amount']))
		return redirect(url_for('feed'))
	if request.method=='GET':
		food_name = query_by_id(food_id).name
		return render_template('edit.html', name=food_name,donation_id=food_id)

@app.route('/edit_request/<int:request_id>', methods=['GET','POST'])
def edit_request(request_id):
	if request.method=='POST':
		update_request(request_id,int(request.form['amount']))
		return redirect(url_for('account_reciever'))
	if request.method=='GET':
		request_name = query_request_by_id(request_id).name
		return render_template('edit_request.html', name=request_name,request_id=request_id)

@app.route('/logout')
def logout():
	del login_session['email']
	if 'donor_name' in login_session.keys(): 
		del login_session['donor_name']
	if 'reciever_name' in login_session.keys():
		del login_session['reciever_name']
	return redirect(url_for('home'))

@app.route('/delete_donation/<int:donation_id>', methods=['GET'])
def delete_donation_route(donation_id):
	if request.method=='GET':
		delete_donation(donation_id)
		return redirect(url_for('feed'))

@app.route('/delete_request/<int:request_id>', methods=['GET'])
def delete_request_route(request_id):
	if request.method=='GET':
		delete_request(request_id)
		return redirect(url_for('account_reciever'))

@app.route('/request_feed',methods=['GET'])
def request_feed():
	if request.method=='GET':
		donor=query_donors_by_email(login_session['email'])
		return render_template('requests_feed.html', requests=query_all_requests(), donor=donor)
















if __name__ == "__main__":
	app.run(debug=True)
