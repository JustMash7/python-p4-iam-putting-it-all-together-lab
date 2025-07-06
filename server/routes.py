# server/routes.py
from flask import request, session, jsonify
from flask_restful import Resource
from server.extensions import db, api, bcrypt
from .models import User, Recipe

class Signup(Resource):
    def post(self):
        data = request.get_json()
        
        # Validate required fields
        required = ['username', 'email', 'password']
        if not all(field in data for field in required):
            return {'error': 'Missing required fields'}, 400
        
        # Check if user exists
        if User.query.filter((User.username == data['username']) | (User.email == data['email'])).first():
            return {'error': 'Username or email already exists'}, 400
        
        # Create new user
        new_user = User(
            username=data['username'],
            email=data['email'],
            _password_hash=bcrypt.generate_password_hash(data['password']).decode('utf-8')
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Set session after successful signup
        session['user_id'] = new_user.id
        
        return new_user.to_dict(), 201

class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data.get('username')).first()
        
        if user and bcrypt.check_password_hash(user._password_hash, data.get('password')):
            # Set session on successful login
            session['user_id'] = user.id
            return user.to_dict(), 200
        
        return {'error': 'Invalid credentials'}, 401

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Unauthorized'}, 401
            
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404
            
        return user.to_dict(), 200

class Logout(Resource):
    def delete(self):
        if 'user_id' in session:
            session.pop('user_id')
            return {}, 204  # No content
        return {'error': 'Unauthorized'}, 401

class Recipes(Resource):
    def get(self):
        # Add session check
        if 'user_id' not in session:
            return {'error': 'Unauthorized'}, 401
            
        # Only get recipes for logged in user
        user = User.query.get(session['user_id'])
        recipes = [recipe.to_dict() for recipe in user.recipes]
        return recipes, 200
    
    def post(self):
        # Add session check
        if 'user_id' not in session:
            return {'error': 'Unauthorized'}, 401
            
        data = request.get_json()
        
        # Validate required fields
        required = ['title', 'instructions']
        if not all(field in data for field in required):
            return {'error': 'Missing required fields'}, 400
        
        # Create new recipe associated with logged in user
        new_recipe = Recipe(
            title=data['title'],
            instructions=data['instructions'],
            minutes_to_complete=data.get('minutes_to_complete'),
            user_id=session['user_id']  # Use session user ID
        )
        
        db.session.add(new_recipe)
        db.session.commit()
        
        return new_recipe.to_dict(), 201

# Add resources to API
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(CheckSession, '/check_session')
api.add_resource(Logout, '/logout')
api.add_resource(Recipes, '/recipes')