import requests
from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from .database import Base,engine,SessionLocal
from .schemas.user import UserRegister ,UserLogin
from .schemas.analyse import analyzeRequest , analyzeResponse
from .models.Users import USER
from .Crud.crud_user import create_user
from .core.security import verify_password_hash ,create_token ,verify_token
from .services.service_HF import ZS_Classify
from .services.service_Gemini import gemini_analysis
from .core.config import SECRET_KEY
from jose import jwt 
from fastapi.security import HTTPBearer, HTTPBasicCredentials 




type_token = HTTPBearer()
app = FastAPI(title="Plateforme Fullstack d’Orchestration IA ")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try :
        yield db
    finally :
        db.close()

db = SessionLocal()


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

async def analyze_text(request: analyzeRequest,token = Depends(verify_token)) :
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


# endpoint /analyze for test HTTPBasicCredentials
@app.post("/test_analyse",response_model=analyzeResponse)

async def analyze_text(request: analyzeRequest,token : HTTPBasicCredentials=Depends(type_token)) :
    my_token = token.credentials
    token_decode = jwt.decode(my_token,SECRET_KEY )
  
    if token_decode :
       text = request.text
       # Appel à la service hagging face
       labels = ["Finance", "RH", "IT", "Opérations","Marketing","Commerce"]  
       HF_result = ZS_Classify(text,labels)
       categorie = HF_result["categorie"]
       score = round(HF_result["score"] * 100, 2)
       
       # Appel à la service Gemini
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
    
    else : 
        return {"message": "Token d'authentification manquant"}