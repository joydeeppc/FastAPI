## This file contains some utility fucntions
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")   ## All we're doing right here is we're telling past lib, what is the default hashing algorithm, or what hashing algorithm do we want to use? In this case, we want to use bcrypt.

## Hash the password 
def hash(password:str):
    return pwd_context.hash(password)        

## The below fucntion is going to take in the raw password, the password attempt, it's going to hash it for us, and then it's going to compare it to the hashed passowd in the database.
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)  ## verify method is used here