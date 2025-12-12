from sqlalchemy.orm import Session
from api_app.models.AnalysisLog import AnalysisLog
import json





def save_analysis_log(user_id : int, input_text, analysis_result: dict,db):
    """
    Sauvegarde  logs d'analyse pour un utilisateur dans la table analysis_logs.

    """
    log = AnalysisLog( user_id=user_id, input_text=input_text,analysis_result=json.dumps(analysis_result))
    db.add(log)
    db.commit()
    db.refresh(log)
