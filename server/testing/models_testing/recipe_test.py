import pytest
from sqlalchemy.exc import IntegrityError
from server.config import app
from extensions import db
from models import  Recipe, User  

@pytest.mark.usefixtures('session')
class TestRecipe:
    '''Recipe in models.py'''

    def test_has_attributes(self):
        '''has attributes title, instructions, and minutes_to_complete.'''
        with app.app_context():
            # Create user first
            user = User(
                username="testuser",
                email="test@example.com",
                password="password"
            )
            db.session.add(user)
            db.session.commit()
            
            # Create recipe associated with user
            recipe = Recipe(
                title="Delicious Shed Ham",
                instructions="""Or kind rest bred with am shed then. In""" + \
                    """ raptures building an bringing be. Elderly is detract""" + \
                    """ tedious assured private so to visited. Do travelling""" + \
                    """ companions contrasted it. Mistress strongly remember""" + \
                    """ up to. Ham him compass you proceed calling detract.""" + \
                    """ Better of always missed we person mr. September""" + \
                    """ smallness northward situation few her certainty""" + \
                    """ something.""",
                minutes_to_complete=60,
                user_id=user.id  # Associate with user
            )

            db.session.add(recipe)
            db.session.commit()

            new_recipe = Recipe.query.filter(Recipe.title == "Delicious Shed Ham").first()

            assert new_recipe.title == "Delicious Shed Ham"
            assert new_recipe.instructions == """Or kind rest bred with am shed then. In""" + \
                """ raptures building an bringing be. Elderly is detract""" + \
                """ tedious assured private so to visited. Do travelling""" + \
                """ companions contrasted it. Mistress strongly remember""" + \
                """ up to. Ham him compass you proceed calling detract.""" + \
                """ Better of always missed we person mr. September""" + \
                """ smallness northward situation few her certainty""" + \
                """ something."""
            assert new_recipe.minutes_to_complete == 60
            assert new_recipe.user_id == user.id  # Verify association

    def test_requires_title(self):
        '''requires each record to have a title.'''
        with app.app_context():
            # Create user
            user = User(
                username="testuser",
                email="test@example.com",
                password="password"
            )
            db.session.add(user)
            db.session.commit()
            
            # Create recipe without title
            recipe = Recipe(
                instructions="x" * 50,  # Valid instructions
                minutes_to_complete=60,
                user_id=user.id
            )
            
            with pytest.raises(IntegrityError):
                db.session.add(recipe)
                db.session.commit()

    def test_requires_50_plus_char_instructions(self):
        '''requires instructions to be at least 50 characters.'''
        with app.app_context():
            # Create user
            user = User(
                username="testuser",
                email="test@example.com",
                password="password"
            )
            db.session.add(user)
            db.session.commit()
            
            # Create recipe with short instructions
            recipe = Recipe(
                title="Short Instructions Recipe",
                instructions="x" * 49,  # Too short (49 chars)
                minutes_to_complete=60,
                user_id=user.id
            )
            
            with pytest.raises(IntegrityError):
                db.session.add(recipe)
                db.session.commit()