from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from .database import Base,engine,SessionLocal
from .schemas.userRegister import UserRegister
from .models.Users import USER
from .outils.create_user import create_user





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
   return True