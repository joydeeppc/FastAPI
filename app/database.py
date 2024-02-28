# This file handles our database connection 

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor                   
import time
from .config import settings


# Then we need to specify our connection string- where is our postgress database located?

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'  ## this is the format
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# Create an engine- it is responsible for sqlalchemy to connect to postgress database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# When we actually want to talk to the SQL database we make use of a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define our base class. And so all of the models that we define to actually create our tables in Postgres, they're going to be extending this base class.
Base = declarative_base()

# Dependency
# Session object is kind of what's responsible for talking with the databases.so we created this function where we actually get a connection to our database, or get a session to our database. And so every time we get a request, we're going to get a session, where we will be able to send SQL statements to it. And then after that request is done, we'll then close it out. 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
    
#         try:
#             conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user='postgres', password = 12345678, cursor_factory= RealDictCursor)    ## cursor_factory= RealDictCursor will give the column name and the values.
#             cursor = conn.cursor()                  ## this will run the sql statements
#             print("Database connection was successfull")
#             break
            
        
#         except Exception as error:
#             print("Connection to database failed")
#             print(f"Error : {error}")
#             time.sleep(2)                   ##set timer to restart
 

        