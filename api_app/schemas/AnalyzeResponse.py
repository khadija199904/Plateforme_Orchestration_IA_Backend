from pydantic import BaseModel

class analyzeResponse(BaseModel):
    categorie: str
    score: float  
    resume: str
    ton: str
    
