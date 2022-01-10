from enum import unique
from flask import Flask, render_template, flash, redirect, url_for
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from data import posts
from forms import RegistrationForm, LoginForm
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '5cdbe643ff49dc0edf15d972114600a0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='about')

@app.route("/register", methods=['get', 'post'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Registration', form=form)

@app.route("/login", methods=['get', 'post'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@siraj.com' and form.password.data == 'password':
            flash('you have been loged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('login unsuccessful, please check your username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


import time
import json
@app.route("/time")
def timeCurent():
    named_tuple = time.localtime() # get struct_time
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
    return render_template('time.html', current_time = time_string)


if __name__ == '__main__':
    app.run(debug = True)