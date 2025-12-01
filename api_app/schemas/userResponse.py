from pydantic import BaseModel ,Field
from datetime import datetime


class UserResponse(BaseModel):
    username: str
    password_hash :str
    createdat : datetime=Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True