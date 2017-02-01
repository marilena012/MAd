from sqlalchemy import Column, ForeignKey, Integer, String, Table, BOOLEAN, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String())
    password = Column(String())
    birthday = Column(Date())
    gender = Column(String())
    country = Column(String())
    diseasesList = relationship("List")
    symptomsList = relationship("List")
    treatmentList = relationship("List")
    diseasesSearch = relationship("List")
    symptomsSearch = relationship("List")
    treatmentSearsh = relationship("List")


class List(Base):
    __tablename__ = 'list'
    name = Column(Integer, primary_key=True)

path = sys.argv[0].replace('/', '\\')
path = path.rsplit('\\', 1)
if len(path) != 2:
    path = os.getcwd()
else:
    path = path[0]

engine = create_engine('sqlite:///' + os.path.join(path, 'mad.db'))

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
