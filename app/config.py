from pydantic_settings import BaseSettings


##We are using this because if we setup the environment variable file, it will take everything as strign. So for typecasting we are using this
class Settings(BaseSettings):
    database_hostname: str
    database_port :str
    database_password :str
    database_name :str
    database_username :str 
    secret_key : str 
    algorithm: str
    access_token_expire_minutes: int


    ## This tells the pydantic to import from our .env file
    class Config:
        env_file = ".env"


##Creating an instance of the class Settings
settings = Settings()
