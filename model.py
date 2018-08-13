from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

# Place your database schema code here
class Donation(Base):
	__tablename__="donations"
	id=Column(Integer,primary_key=True)
	name=Column(String)
	amount=Column(Integer)
	expiration_date=Column(Date)
# Example code:
class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key = True)
    name = Column(String)
    year = Column(Integer)

    def __repr__(self):
        return ("Student name: {}, Student year:{}".format(self.name, self.year))