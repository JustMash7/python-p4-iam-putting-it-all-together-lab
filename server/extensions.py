# server/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

db = SQLAlchemy()
api = Api()
bcrypt = Bcrypt()
migrate = Migrate()