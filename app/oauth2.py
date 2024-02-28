from jose import JWSError,jwt

from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from . import schemas,database,models
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')   ## here the tokenUrl is the endpoint of our login router.What ever it is.


## Requiements - SECRET_KEY, ALGORITHM, Expiration time(till when should an user should be login)

## SECRET_KEY can be anything. It can be a plain text like "Hello"
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()          ## we have made the copy of the actual data so that if we do some manipulation in future it will not change the actual data 

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp" : expire})          ## we're just adding that extra property into the into all of that data that we want to encode into our JWT

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY,algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_access_token(token : str, credentials_exception):
    
    ##anytime you're working with code that can error out, you want to do a try except block.
    try:
        ## This will store all of our payload data
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
        ## To extract the data
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id = id)
    except JWSError:
        raise credentials_exception
    
    return token_data
    
## we can pass this as a dependency into any one of our path operations. And when we do that, what it's going to do is it's going to take the token from the request automatically extract the ID for us,  it's going to verify that the token is correct by calling the verify access token. And then it's going to extract the ID.         
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token =  verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id== token.id).first()
    
    # return verify_access_token(token, credentials_exception)
    return user
