# Every model represents a table in our database

from .database import Base
from sqlalchemy import Column, Integer, String, Boolean,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

# We're going to create a model for posts. This will create a table in postgress
class Post(Base):
    __tablename__ = "post"

    #define all the columns
    id = Column(Integer, primary_key= True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default = 'TRUE', nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False,server_default=text('now()') )
    owner_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"), nullable = False)  ## here users is the table name. It will not be the class

    ##Set up a relationship. This reletionship is not a foreign key, it does nothing in the database whatsoever.what it does is it'll tell SQL alchemy to automatically fetch some piece of information based off of the relationship.
    owner = relationship("User")  ## Here User is the class not the table name. The owner is used to get the email of the user.

class User(Base):
    __tablename__= "users"
    id = Column(Integer, primary_key= True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False )
    created_at = Column(TIMESTAMP(timezone=True), nullable = False,server_default=text('now()') )


class Vote(Base):
    __tablename__ = "votes"
    user_id =  Column(Integer,ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)   
    post_id = Column(Integer,ForeignKey("post.id", ondelete="CASCADE"), primary_key=True)   


