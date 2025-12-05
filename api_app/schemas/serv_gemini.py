from pydantic import BaseModel

class GeminiResponse(BaseModel):
    text_resume : str
    ton : str

    class Config:
        from_attributes = True
