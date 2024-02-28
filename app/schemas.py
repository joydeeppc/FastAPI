from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint


# class Post(BaseModel):
#     title : str
#     content : str
#     published : bool = True



class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True


# class CreatePost(BaseModel):
#     title : str
#     content : str
#     published : bool = True


# class UpdatePost(BaseModel):  
#     title : str
#     content : str
#     published : bool  
    
## here we are using the concept of inheritance   
class PostCreate(PostBase):                   
    pass                      

## The below shcema is for what we want the user to see. we dont want them to see their passwords back. We will user it in our path operation as response model
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at : datetime
    
    class Config:
        orm_mode : True

    
## This is the model which is used for sending the response to the user since we might not need to send everything to user
class Post(PostBase):
    id: int
    # title: str
    # content: str
    # published: bool = True
    created_at : datetime
    owner_id : int

    ## below owner is added to get the email of the user who created the post. Since thats how the social media platform works. It gives the username
    owner : UserOut
    ## we are using the below config class because it pydantic model only understand dictionary.So this will help to ignore the fact that what we recieved is not dictionary but sqlalchemy model
    class Config:
        orm_mode : True

## We have creted this class because in the response we were getting different structure while we were doing the joins. 
class PostOut(BaseModel):
    Post : Post
    votes : int

    class Config:
        orm_mode : True        

## Here we are creating the schema of the user 
class UserCreate(BaseModel):
    email: EmailStr
    password: str



## the below schema is used for the authentication router 
class UserLogin(BaseModel):
    email: EmailStr
    password: str

## Schema for the token
class Token(BaseModel):
    access_token: str
    token_type : str

## Schema for the token data - the data that we embedded into our access token
class TokenData(BaseModel):
    id : Optional[int] = None               #### its an issue. In video it was str but I have changed it to int then it worked
    # id : Optional[str] = None 


## This schema is for vote
class Vote(BaseModel):
    post_id : int
    dir :   conint(le=1)    ##here conint will ensure that the entired integer is either 0 or 1. but it also allows negative number aswell

        
        