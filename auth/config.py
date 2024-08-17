import datetime
import os

SECRET_KEY = os.getenv(
    key="SECRET_KEY",
    default="a23a5505463367a8aaeb26ab8f23a98e3893a96bac1895aa8a8d6c195ac5bee4"
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {"admin": {"username": "admin", "password": "presale"}}


def get_token_expiration():
    return datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
