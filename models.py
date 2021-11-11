# Standard library imports
import datetime

# Database config imports
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Table modeling imports
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

# Hash
from werkzeug.security import generate_password_hash, check_password_hash

# Flask Login
from main import login_manager
from flask_login import UserMixin

uri = 'sqlite:///database.db'
engine = create_engine(uri)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Create table Base class and set .query property for searches
Base = declarative_base()
Base.query = Session.query_property()


@login_manager.user_loader
def get_user(user_id):
    return User.query.filter_by(id=user_id)

# @login_manager.user_loader
# def is_active(self):
#     return True

# @login_manager.user_loader
# def is_authenticated(self):
#     return True

# @login_manager.user_loader
# def is_anonymous(self):
#     return False


class User(Base, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String(255))
    password = Column(String(255))

    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)


def initialize_db():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    initialize_db()
