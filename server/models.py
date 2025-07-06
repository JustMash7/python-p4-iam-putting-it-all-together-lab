# server/models.py
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
import extensions as extensions  

class User(extensions.db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = extensions.db.Column(extensions.db.Integer, primary_key=True)
    username = extensions.db.Column(extensions.db.String(80), nullable=False, unique=True)
    _password_hash = extensions.db.Column(extensions.db.String(128), nullable=False)
    image_url = extensions.db.Column(extensions.db.String(255))
    bio = extensions.db.Column(extensions.db.String(255))

    recipes = extensions.db.relationship('Recipe', backref='user', lazy=True)

    serialize_rules = ('-_password_hash', '-recipes.user')

    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password hashes may not be viewed.')

    @password_hash.setter
    def password_hash(self, password):
        # Validate password before hashing
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one number")
        if not any(char.isupper() for char in password):
            raise ValueError("Password must contain at least one uppercase letter")
            
        self._password_hash = extensions.bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return extensions.bcrypt.check_password_hash(self._password_hash, password)

    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError("Username must be present")
        return username

class Recipe(extensions.db.Model, SerializerMixin):
    __tablename__ = 'recipes'

    id = extensions.db.Column(extensions.db.Integer, primary_key=True)
    title = extensions.db.Column(extensions.db.String(255), nullable=False)
    instructions = extensions.db.Column(extensions.db.Text, nullable=False)
    minutes_to_complete = extensions.db.Column(extensions.db.Integer)
    user_id = extensions.db.Column(extensions.db.Integer, extensions.db.ForeignKey('users.id'), nullable=False)

    serialize_rules = ('-user.recipes', '-user._password_hash')

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Title must be present")
        return title

    @validates('instructions')
    def validate_instructions(self, key, instructions):
        if len(instructions) < 50:
            raise ValueError("Instructions must be at least 50 characters long")
        return instructions

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "instructions": self.instructions,
            "minutes_to_complete": self.minutes_to_complete,
            "user_id": self.user_id
        }