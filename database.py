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

def add_donor(name, email, password, area, adress, phone_number):
	donor_object = Donor(
		name=name,
		email = email,
		password = password,
		area = area,
		adress=adress,
		phone_number=phone_number)
	session.add(donor_object)
	session.commit()

def delete_donation(donation_id):
	session.query(Donation).filter_by(
		donation_id=donation_id).delete()
	session.commit()

def query_all():
	donations = session.query(Donation).all()
	return donations

def query_by_id(donation_id):
    donation = session.query(Donation).filter_by(
        donation_id=donation_id).first()
    return donation
