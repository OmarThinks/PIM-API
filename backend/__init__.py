SECRET="change me"

from datetime import timedelta
import secrets


EXPIRATION_AFTER= timedelta(days=7)

#from flask_sqlalchemy import SQLAlchemy

#db = SQLAlchemy()
from sqlalchemy import create_engine
engine = create_engine('sqlite:///databases/database.sqlite')
from sqlalchemy.orm import sessionmaker
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
#from models_new import (User, Product)
