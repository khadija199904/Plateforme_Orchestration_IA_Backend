from .hashing_password import get_password_hash
from api_app.schemas.userRegister import UserRegister
from api_app.models.Users import USER

def create_user (user_data : UserRegister):
    hashed_password = get_password_hash(user_data.password)
    new_user = USER(username=user_data.username,password_hash=hashed_password)
    return new_user