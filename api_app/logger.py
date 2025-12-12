import logging
import time
from fastapi import HTTPException

# Logger global orchestration
logger = logging.getLogger("Orchestration_Complete")
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler("Analysis.log", mode="a", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


# Fonction utilitaire de logging pour l’orchestration

def log_task(task_name, func, *args, **kwargs):

    start = time.time()
    
    logger.debug(f"DEBUG | Entrée dans Pipeline IA : Analyse texte avec Fusion HF + Gemini ")
    
    logger.info(f"ORCHESTRATION | Début de la tâche : {task_name}")

    

    try:
        # Exécution réelle
        result = func(*args, **kwargs)
        return result

    except HTTPException as e:
        # ERROR pour exceptions  gérées
        logger.error(f"ERROR | Tâche : {task_name} | HTTPException : {e.detail}")
        raise e

    except Exception as e:
        # CRITICAL pour erreurs inattendues
        logger.critical(f"ERREUR CRITIQUE | Tâche : {task_name} | Erreur : {e}")
        raise e
    
    finally:
        end = time.time()
        duration_ms = (end - start) * 1000
        duration_s = end - start  
        # Performance
        logger.info(
            f"PERFORMANCE | Fin : {task_name} | "
            f"Durée : {duration_ms:.2f} ms ({duration_s:.2f} s)"
        )