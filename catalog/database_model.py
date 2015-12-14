#!/usr/bin/python
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()


class User(Base):
    """User database class.

    This class can be used to store logged in user information. Attributes
    match properties available once a user has logged in via Google OAuth.

    Attributes:
        id: Google Account Id
        name: Users name as listed in their Google account information
        email: Users Google email address
        picture: Google profile picture URL
    """

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'picture': self.picture,
        }


class Category(Base):
    """Base class for item categories.

    Class that stores basic information about item categories.

    Attributes:
        id: Category Id
        name: Name of the item category
        description: Description of items in the category
    """

    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(500))
    # background image

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }


class CategoryItem(Base):
    """Class for individual items

    Base class used to store information about individual items. Each item
    relates to the category it belongs too. User columns are not used in this
    version as the application doesn't store user infomation in the database.

    Attributes:
        id: Unique Id of the item
        name: Item name
        description: Brief description of the item
        image_url: URL to an image of the item
        image_caption: Short description of the item image
        category_id: Id of the category the item belongs too
        category: Foreign Key relationship to the parrent category
        meaning: English translation of Greek name of the Dinosaur
        period: Which historic period did the Dinosaur exist
        diet: Food the Dinosaur ate
    """

    __tablename__ = 'category_item'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(1000))
    image_url = Column(String(500))
    image_caption = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    # Dinosaur specific columns
    meaning = Column(String(250))
    period = Column(String(250))
    diet = Column(String(250))
    # user_id = Column(Integer, ForeignKey('user.id'))
    # user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image': self.image_url,
            'caption': self.image_caption,
            'meaning': self.meaning,
            'period': self.period,
            'diet': self.diet,
            'category': self.category_id,
        }


# Create SQLite DB
engine = create_engine('sqlite:///itemcatalogue.db')


Base.metadata.create_all(engine)
