from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from ..schemas.user import UserRegister ,UserLogin
from ..models.Users import USER
from ..Crud.crud_user import create_user
from ..core.security import verify_password_hash ,create_token
from ..dependencies import get_db

router = APIRouter( prefix="/auth", tags=["Authentication"])

@router.post('/register')
async def Register(user : UserRegister ,db: Session = Depends(get_db)) :
   existing_user = db.query(USER).filter(USER.username == user.username ).first()
   if existing_user:
         raise HTTPException(status_code=400,detail="Compte Déja existe")
   new_user = create_user(user)
   print("Nouvel utilisateur créé :", new_user)
   print(new_user)
   db.add(new_user)
   db.commit()
   db.refresh(new_user)
   return {"message": "Compte créé avec succès", "username": new_user.username}



# Endpoint login protégée

@router.post("/login") 
async def login(user : UserLogin,db: Session = Depends(get_db)):
 
     user_data = db.query(USER).filter(USER.username == user.username ).first()
     
     if not user_data or not verify_password_hash(user.password,user_data.password_hash):
        raise HTTPException(status_code=401,detail="Access Failed (Incorrect username or password)")
     
     token = create_token(user_data) 
     return {"access_token": token }
 
