from pydantic import BaseModel

class analyzeRequest(BaseModel):
    text: str