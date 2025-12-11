from pydantic import BaseModel,ConfigDict

class GeminiResponse(BaseModel):
    text_resume : str
    ton : str

    model_config = ConfigDict(
        extra="forbid",  # interdit les champs supplémentaires
        validate_assignment=True
    )
