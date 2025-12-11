from pydantic import BaseModel ,Field
from datetime import datetime

class UserRegister(BaseModel):
    email : str
    username :str
    password : str


class UserLogin(BaseModel):
    username :str
    password : str


# class User_db(BaseModel):
#     username: str
#     password_hash :str
#     createdat : datetime=Field(default_factory=datetime.utcnow)

#     class Config:
#         from_attributes = True