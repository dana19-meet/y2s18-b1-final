from model import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
import datetime

engine = create_engine('sqlite:///students.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

def add_donation(name, amount, expiration_date, donor):
	donation_object = Donation(
		name= name,
		amount=amount,
		expiration_date=expiration_date,
		donor=donor)
	session.add(donation_object)
	session.commit()

def add_donor(name, email, password, area, address, telephone):
	donor_object = Donor(
		name=name,
		email = email,
		password = password,
		area = area,
		address=address,
		telephone=telephone)
	session.add(donor_object)
	session.commit()

def add_reciever(reciever_name, email, password, area, telephone):
	reciever_object = Reciever(
		reciever_name=reciever_name,
		email = email,
		password = password,
		area = area,
		telephone=telephone)
	session.add(reciever_object)
	session.commit()

def delete_donation(donation_id):
	session.query(Donation).filter_by(
		donation_id=donation_id).delete()
	session.commit()


def query_all_donates():
	donations = session.query(Donation).all()
	return donations

def query_all_donors():
	donors = session.query(Donor).all()
	return donors

def query_by_id(donation_id):
    donation = session.query(Donation).filter_by(
        donation_id=donation_id).first()
    return donation

def query_donors_by_email(email):
	donor = session.query(Donor).filter_by(email=email).first()
	return donor

def query_donors_by_id(donor_id):
	donor = session.query(Donor).filter_by(donor_id=donor_id).first()
	return donor


def query_recievers_by_email(email):
	reciever = session.query(Reciever).filter_by(email=email).first()
	return reciever

def delete_donations_by_exp(expiration_date):
    session.query(Donation).filter_by(
        expiration_date=expiration_date).delete()
    session.commit()

def query_donations_by_donorid(donor_id):
	donations = session.query(Donation).filter_by(donor_id=donor_id).all()
	return donations

def update_donation(donation_id,expiration_date,amount):
	donation=session.query(Donation).filter_by(donation_id=donation_id).first()
	donation.expiration_date=expiration_date
	donation.amount=amount
	session.commit()
