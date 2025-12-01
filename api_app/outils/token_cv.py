from api_app.schemas.userRegister import UserRegister
from fastapi import Header
from dotenv import load_dotenv
import os
from jose import jwt 
from fastapi import HTTPException
load_dotenv
 

 # Configuration de JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def create_token (user:UserRegister,) :
   
    payload = { "Username" : user.username}
    token = jwt.encode(payload,key=SECRET_KEY,algorithm=ALGORITHM)
    return token




# verificatin de token cree en login
def verify_token(token : str = Header()):
  try:
      token_decoded = jwt.decode(token=token,key=SECRET_KEY,algorithms=[ALGORITHM])
      return token_decoded
  except :
      #  GESTION TOKEN MANQUANT
      raise HTTPException(status_code=401,detail="Token d'authentification manquant")