from fastapi import APIRouter, Depends, HTTPException
from ..schemas.analyse import analyzeRequest, analyzeResponse
from ..services.analyse_text import analyse
from ..core.security import verify_token



router = APIRouter( tags=["Analysis"])

# endpoint /analyse
@router.post("/analyse",response_model=analyzeResponse)

async def analyze_text(request: analyzeRequest,token = Depends(verify_token)) :
    text = request.text
    global_result = analyse(text)
    return analyzeResponse(**global_result)
