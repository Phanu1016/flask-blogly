import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

"""Models for Blogly."""
class User(db.Model):
    __tablename__ = 'users'

    def __repr__(self):
        return f'<User id={self.id} first_name={self.first_name} last_name={self.last_name} image_url={self.image_url}>'

    id = db.Column(db.Integer,
                   primary_key=True)

    first_name = db.Column(db.String(50),
                           nullable=False)
                           
    last_name = db.Column(db.String(50),
                          nullable=False)

    image_url = db.Column(db.String(200),
                          nullable=False,
                          default='https://i.imgur.com/iUG6xnZ.png')

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(10000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref='posts')

