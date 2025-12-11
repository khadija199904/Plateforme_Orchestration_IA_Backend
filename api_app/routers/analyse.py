from fastapi import APIRouter, Depends, HTTPException
from ..schemas.analyse import analyzeRequest, analyzeResponse
from ..services.analyse_text import analyse
from ..core.security import verify_token
from ..logger import logger ,log_task


router = APIRouter( tags=["Analysis"])

# endpoint /analyse
@router.post("/analyse",response_model=analyzeResponse)

async def analyze_text(request: analyzeRequest,token = Depends(verify_token)) :
    text = request.text
    
    try:
        #  analyse avec logging
        global_result = log_task( "Analyse texte ", analyse, text)
        return analyzeResponse(**global_result)
    except HTTPException as e:
        # On renvoie simplement l'exception déjà levée par le service HF
        raise e
    except Exception:
        # Autres erreurs critiques
        raise HTTPException(status_code=500, detail="Erreur critique lors de l'analyse")
