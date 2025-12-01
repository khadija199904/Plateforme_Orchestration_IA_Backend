from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from .database import Base,engine,SessionLocal
from .schemas.userRegister import UserRegister
from .schemas.userLogin import UserLogin
from .models.Users import USER
from .outils.create_user import create_user
from .outils.password_hash_cv import verify_password_hash
from .outils.token_cv import create_token





app = FastAPI(title="Plateforme Fullstack d’Orchestration IA ")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try :
        yield db
    finally :
        db.close()


@app.post('/register')
async def Register(user : UserRegister ,db: Session = Depends(get_db)) :
   existing_user = db.query(USER).filter(USER.username == user.username ).first()
   if existing_user:
         raise HTTPException(status_code=400,detail="Username Déja existe")
   
   new_user = create_user(user)
   print(new_user)
   db.add(new_user)
   db.commit()
   db.refresh(new_user)
   return {"message": "Compte créé avec succès", "username": new_user.username}

# Endpoint login protégée

@app.post("/login") 
async def login(user : UserLogin,db: Session = Depends(get_db)):
     
     user_data = db.query(USER).filter(USER.username == user.username ).first()
     # Vérification username et password
     if not user_data or not verify_password_hash(user.password,user_data.password_hash):
        raise HTTPException(status_code=401,detail="Access Failed (Incorrect username or password)")
     
     token = create_token(user_data) 
     return {"access_token": token }
     