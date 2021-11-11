from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin

from flask_login import login_user, logout_user

# Database config imports
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Table modeling imports
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

# Hash
from werkzeug.security import generate_password_hash, check_password_hash

# App setup
app = Flask(__name__)
app.secret_key = '13fe4033cf1aba34a07d77e7b249a936831439fbb5881d7b3b1b32834e27a8a7'

# Login manager setup
login_manager = LoginManager()
login_manager.init_app(app)

# MODELS ==================================

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


# END MODELS ==============================


# class User(UserMixin):
#     pass


@login_manager.user_loader
def load_user(user_id):
    return get_user(user_id)


@app.route('/')
def home():
    return render_template('home.html.jinja')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if not (user or user.verify_password(password)):
            return render_template('login.html.jinja', error=True)

        login_user(user)

        return redirect(url_for('home'))

    return render_template('login.html.jinja', error=False)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Erro 1: posso criar várias contas com o mesmo email
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User(email, password)

        with Session() as session:
            session.add(user)
            session.commit()

        print("Email: ", email)
        print("Password: ", password)

        return redirect(url_for('signup'))

    return render_template('signup.html.jinja')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
