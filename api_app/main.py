from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from .database import Base,engine,SessionLocal
from .schemas.userRegister import UserRegister
from .schemas.userLogin import UserLogin
from .schemas.AnalyzeResponse import analyzeResponse
from .schemas.AnalyseRequest import analyzeRequest
import requests
from .models.Users import USER
from .outils.create_user import create_user
from .outils.password_hash_cv import verify_password_hash
from .outils.token_cv import create_token
from .services.service_HF import ZS_Classify
from .services.service_Gemini import gemini_analysis





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


# endpoint /analyze

@app.post("/analyse",response_model=analyzeResponse)

async def analyze_text(request: analyzeRequest) :
    text = request.text

    labels = ["Finance", "RH", "IT", "Opérations","Marketing","Commerce"]  
    HF_result = ZS_Classify(text,labels)
    categorie = HF_result["categorie"]
    score = round(HF_result["score"] * 100, 2)
    Gemini_result = gemini_analysis(text,categorie)
    resume = Gemini_result["text_resume"]
    ton = Gemini_result ["ton"]
    
    global_result = {
    "categorie": categorie,
    "score": score,
    "resume": resume,
    "ton": ton
    
      }
    return analyzeResponse(**global_result)