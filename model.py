from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

# Place your database schema code here
class Donation(Base):
	__tablename__="donations"
	donation_id=Column(Integer,primary_key=True)
	donor_id = Column(Integer, ForeignKey('donors.donor_id'))
	name=Column(String)
	amount=Column(Integer)
	expiration_date=Column(Date)
	email=Column(String)
	donor = relationship("Donor", back_populates = "donation")

class Donor(Base):
	__tablename__="donors"
	donor_id=Column(Integer,primary_key=True)
	name=Column(String)
	email=Column(String)
	password=Column(String)
	area=Column(String)
	address=Column(String)
	telephone=Column(String)
	donation = relationship("Donation", back_populates = "donor")

class Reciever(Base):
    __tablename__ = "recievers"
    reciever_id = Column(Integer, primary_key = True)
    reciever_name = Column(String)
    email = Column(String)
    password = Column(String)
    area = Column(String)
    telephone = Column(String)

    def __repr__(self):
        return ("Student name: {}, Student year:{}".format(self.name, self.year))