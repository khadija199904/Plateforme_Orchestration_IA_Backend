from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies import get_db
from ..schemas.analyse import analyzeRequest, analyzeResponse
from ..outils.analyse_text import analyse
from ..core.security import verify_token
from ..logger import logger ,log_task
from ..outils.save_analysis import save_analysis_log
from pydantic import ValidationError
from ..models.Users import USER


router = APIRouter( tags=["Analysis"])

# endpoint /analyse
@router.post("/analyse",response_model=analyzeResponse)

async def analyze_text(request: analyzeRequest,token = Depends(verify_token), db: Session = Depends(get_db)) :
    text = request.text

    username = token["Username"]

    # Chercher l'utilisateur en base
    user = db.query(USER).filter(USER.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    #  Récupérer l'id réel
    user_id = user.id
    
    try:
        #  analyse avec logging
        global_result = log_task( "Analyse texte", analyse, text)
        print(global_result)
        # Sauvegarde dans analysis_logs
         
        save_analysis_log(db=db, user_id=user_id, input_text=text, analysis_result=global_result)

        return analyzeResponse(**global_result)
    
    except ValidationError as e:
        
        raise HTTPException(status_code=422,detail={"message": "Données envoyées invalides","errors": e.errors()})
    
    except HTTPException as e:
        raise e
    
    
