from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str 
    ASYNC_DATABASE_URL: str 
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = '.env'

settings = Settings()
