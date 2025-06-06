from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    release_date = db.Column(db.Date, nullable=True)
    developer = db.Column(db.String(100))
    genre = db.Column(db.String(50))
    platform = db.Column(db.String(100))
    cover_image = db.Column(db.String(200))  

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.String(50), nullable=True)  
    image_url = db.Column(db.String(250), nullable=True)  
    is_featured = db.Column(db.Boolean, default=False)  

    def __repr__(self):
        return f'<News {self.title}>'
