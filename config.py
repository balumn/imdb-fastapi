
from pydantic import BaseSettings

class AuthSettings(BaseSettings):
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Settings(BaseSettings):
    admin: str = "my_username"
    password: str = "my_passw0rd"

admin_user = {
    "my_username": {
        "username": "my_username",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$E/CM.Mq.Bgs3d1o/K/7Cuexa8Oac8IppWuFb81zSjF2RabXwWfySW",
        "disabled": False,
    }
}
