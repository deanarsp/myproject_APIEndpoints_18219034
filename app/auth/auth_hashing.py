from passlib.context import CryptContext

import json

with open("users.json", "r") as read_file:
	user_data = json.load(read_file)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def check_user(username: str, password: str):
    for user in user_data:
        if user["username"] == username and verify_password(password, user['password']):
            return True
    return False