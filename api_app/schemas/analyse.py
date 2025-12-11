from pydantic import BaseModel

class analyzeRequest(BaseModel):
    text: str

class analyzeResponse(BaseModel):
    categorie: str
    score: float  
    resume: str
    ton: str
    