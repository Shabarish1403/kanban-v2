from .database import db
from flask_security import UserMixin, RoleMixin

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, nullable=False ,unique=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean)
    fs_uniquifier = db.Column(db.String, unique=True, nullable=False)
    lists = db.relationship('List', backref='user',cascade='all,delete-orphan')
    
class List(db.Model):
    __tablename__ = 'list'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    update_date = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cards = db.relationship('Card',backref='list',cascade='all,delete-orphan')

class Card(db.Model):
    __tablename__ = 'card'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    deadline = db.Column(db.String, nullable=False)
    toggle = db.Column(db.String, nullable=False)
    create_date = db.Column(db.String, nullable=False)
    complete_date = db.Column(db.String, nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=False)