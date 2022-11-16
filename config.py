from pydantic import BaseSettings


class Settings(BaseSettings):
    # below we are defining env variables and the type for them
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # below we are specifying the file with env variables
    class Config:
      env_file = ".env"

# below we are setting up an instance of the class
settings = Settings()

