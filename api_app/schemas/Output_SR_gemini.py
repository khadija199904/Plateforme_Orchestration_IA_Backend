from pydantic import BaseModel

class OutputGemini(BaseModel):
    text_resume : str
    ton : str

    class Config:
        from_attributes = True

