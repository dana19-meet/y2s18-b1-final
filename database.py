from model import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship

Base=declarative_base()

engine = create_engine('sqlite:///students.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

def add_donation(name, amount, expiration_date):
	donation_object = Donation(
		name= name,
		amount=amount,
		expiration_date=expiration_date)
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

def query_recievers_by_email(email):
	reciever = session.query(Reciever).filter_by(email=email).first()
	return reciever

