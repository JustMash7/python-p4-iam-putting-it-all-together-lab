import os
import sys
from flask import Flask, request, session
from flask_restful import Api, Resource
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
import config  
from models import User, Recipe  

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import extensions after path setup
import extensions as extensions

# Create extensions
api = Api()
migrate = Migrate()

def create_app():
    """Application factory function"""
    app = Flask(__name__)
    app.config.from_object(config.Config)  
    
    # Initialize extensions with app
    extensions.db.init_app(app)
    api.init_app(app)
    migrate.init_app(app, extensions.db)  
    
    # Define Resource classes
    class Signup(Resource):
        def post(self):
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            image_url = data.get('image_url')
            bio = data.get('bio')

            try:
                existing_user = User.query.filter_by(username=username).first()
                if existing_user:
                    return {"error": "Username already exists"}, 422
                
                user = User(
                    username=username,
                    image_url=image_url,
                    bio=bio
                )
                
                user.password_hash = password  
                
                extensions.db.session.add(user)
                extensions.db.session.commit()
                session['user_id'] = user.id
                return user.to_dict(), 201
                
            except ValueError as e:
                extensions.db.session.rollback()
                return {"error": str(e)}, 422
            except IntegrityError:
                extensions.db.session.rollback()  # Fixed typo
                return {"error": "Username already exists"}, 422

    class CheckSession(Resource):
        def get(self):
            user_id = session.get('user_id')
            if not user_id:
                return {"error": "Unauthorized"}, 401
            
            user = User.query.get(user_id)
            if user:
                return user.to_dict(), 200
            return {"error": "User not found"}, 404

    class Login(Resource):
        def post(self):
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            user = User.query.filter_by(username=username).first()
            if user and user.verify_password(password):
                session['user_id'] = user.id
                return user.to_dict(), 200
            return {"error": "Invalid credentials"}, 401

    class Logout(Resource):
        def delete(self):
            if 'user_id' in session:
                session.pop('user_id')
                return '', 204
            return {"error": "Unauthorized"}, 401

    class RecipeIndex(Resource):
        def get(self):
            user_id = session.get('user_id')
            if not user_id:
                return {"error": "Unauthorized"}, 401
            
            recipes = Recipe.query.all()
            return [recipe.to_dict() for recipe in recipes], 200

        def post(self):
            user_id = session.get('user_id')
            if not user_id:
                return {"error": "Unauthorized"}, 401
            
            data = request.get_json()
            title = data.get('title')
            instructions = data.get('instructions')
            minutes_to_complete = data.get('minutes_to_complete')
            
            if not title or not instructions:
                return {"error": "Missing required fields"}, 422

            recipe = Recipe(
                title=title, 
                instructions=instructions, 
                minutes_to_complete=minutes_to_complete, 
                user_id=user_id
            )
            
            try:
                extensions.db.session.add(recipe)  
                extensions.db.session.commit()
                return recipe.to_dict(), 201
            except IntegrityError as e:
                extensions.db.session.rollback()
                return {"error": str(e)}, 422

    # Add resources to API
    api.add_resource(Signup, '/signup')
    api.add_resource(CheckSession, '/check_session')
    api.add_resource(Login, '/login')
    api.add_resource(Logout, '/logout')
    api.add_resource(RecipeIndex, '/recipes')
    
    return app

# Create app instance
app = create_app()

if __name__ == '__main__':
    app.run(port=5555, debug=True)