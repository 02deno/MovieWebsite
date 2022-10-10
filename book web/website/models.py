from flask_login import UserMixin
from sqlalchemy.sql import func 
from . import db 

class Film(db.Model) :
    id = db.Column(db.Integer,primary_key = True)
    movieName= db.Column(db.String(150))
    directorName = db.Column(db.String(150))
    movieText= db.Column(db.String(10000))
    rate = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True),default= func.now())
    image_name = db.Column(db.String(),nullable = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    #not the actual image,name of it
    

class User(db.Model,UserMixin) :
    id = db.Column(db.Integer,primary_key = True)
    first_name = db.Column(db.String(150))
    email = db.Column(db.String(150),unique = True)
    password = db.Column(db.String(150))
    films = db.relationship('Film')

