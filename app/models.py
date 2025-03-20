from flask_login import UserMixin
from . import db, bcrypt  

class User(db.Model, UserMixin):  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_moderator = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=False)
    director = db.Column(db.String(255), nullable=True)
    actors = db.Column(db.Text, nullable=True)
    year = db.Column(db.Integer, nullable=True)
    runtime = db.Column(db.Integer, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    votes = db.Column(db.Integer, nullable=True)
    revenue = db.Column(db.Float, nullable=True)
    metascore = db.Column(db.Integer, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
