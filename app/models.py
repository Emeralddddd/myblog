from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from app import CKEditorField

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def my_posts(self):
        return Post.query.filter(Post.user_id==self.id).order_by(Post.timestamp.desc())

posttags = db.Table('posttags',db.Column('tagid',db.Integer,db.ForeignKey('tag.id')),db.Column('postid',db.Integer,db.ForeignKey('post.id')))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    abs = db.Column(db.String(100))
    body = db.Column(db.String(3000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship('Tag',secondary=posttags,backref=db.backref('post',lazy='dynamic'),lazy='dynamic')
    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Tag(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))

class PostForm(FlaskForm):
    title = TextAreaField('Ttile',validators=[DataRequired()])
    abs =TextAreaField('Abstract')
    post = TextAreaField('Say something', validators=[DataRequired()])
    submit = SubmitField('Submit')

class PostForm1(FlaskForm):
    title = StringField('标题')
    abs = StringField('副标题')
    body = CKEditorField('正文')
    submit = SubmitField('Submit')

class Header:
    def __init__(self, img, title, subTtile):
        self.img = img
        self.title = title
        self.subTitle = subTtile


class Footer:
    def __init__(self, twitter, facebook, github):
        self.twitter = twitter
        self.facebook = facebook
        self.github = github

@login.user_loader
def load_user(id):
    return User.query.get(int(id))