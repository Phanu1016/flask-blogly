"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "Phanuphanu"

connect_db(app)
db.create_all()


@app.route('/')
def home_page():
    """ Redirect to list of users """
    return redirect('/users')

@app.route('/users')
def users():
    """ Show all users """
    users = User.query.all()
    return render_template('users.html', users=users)

# Create new user
@app.route('/users/new')
def create_new_user():
    """ Show an add form for users """
    return render_template('create.html')

@app.route('/users/new', methods=['POST'])
def create_new_user_post():
    """ Process the add form, adding a new user and going back to /users """

    user = User(first_name=request.form['firstName'], last_name=request.form['lastName'], image_url=request.form['imageURL'], )

    db.session.add(user)
    db.session.commit()
    return redirect('/users')

# User Profile
@app.route('/users/<int:user_id>')
def user_profile(user_id):
    """ Show information about the given user """
    user = User.query.get_or_404(user_id)
    return render_template('profile.html', user=user)

@app.route('/users/<int:user_id>/edit')
def user_edit(user_id):
    """ Show the edit page for a user """
    user = User.query.get_or_404(user_id)
    return render_template('profile_edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def user_edit_post(user_id):
    """ Process the edit form, returning the user to the /users page """
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['firstName']
    user.last_name = request.form['lastName']
    user.image_url = request.form['imageURL']

    db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def user_delete(user_id):
    """ Delete the user """
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')



