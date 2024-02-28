from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post,user,auth,vote
from . config import Settings





## This will create all of our models
# models.Base.metadata.create_all(bind=engine)

## app is the fastapi object which we have created
app = FastAPI() 

origins = ["*"]
## This section is fro CORS. Middleware is used in most web framework, Its is a function that runs before every request
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


##all we're doing is we're just grabbing the router object from the post file. And that's essentially going to import all of the specific routes.         
app.include_router(post.router)
##all we're doing is we're just grabbing the router object from the user file. And that's essentially going to import all of the specific routes.                  
app.include_router(user.router)                  
app.include_router(auth.router)  
app.include_router(vote.router)  








    
    