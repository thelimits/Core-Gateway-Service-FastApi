from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    tm_api_server: str
    tm_auth_token: str
    database_password: str
    database_hostname:str
    database_name:str
    database_username:str
    pool_database_max:int
    class Config:
        env_file = ".env"


settings = Settings()

# check
print("tm_api_server:", settings.tm_api_server)
print("tm_auth_token:", settings.tm_auth_token)