# create_db.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create a minimal Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Import models after db is created
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    minutes_to_complete = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

# Create tables
with app.app_context():
    db.drop_all()
    db.create_all()
    print("Database tables created successfully!")
    
    # Add sample data
    user = User(username="testuser", email="test@example.com", password="testpass")
    db.session.add(user)
    db.session.commit()
    
    recipe = Recipe(title="Test Recipe", instructions="Mix ingredients", user_id=user.id)
    db.session.add(recipe)
    db.session.commit()
    print("Sample data added!")