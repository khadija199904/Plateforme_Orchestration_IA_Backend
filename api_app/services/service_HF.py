import os
import requests
from dotenv import load_dotenv
from fastapi import HTTPException
from api_app.core.config import HF_API_TOKEN





if not HF_API_TOKEN:
    raise ValueError("La clé d'API Hugging Face n'est pas définie. Veuillez la mettre dans le fichier .env")
headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}



def ZS_Classify(text,labels):
     
    if not text :
        return None
    API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"

    payload = { "inputs": text, "parameters": { "candidate_labels": labels } }

    try : 

       hf_response = requests.post(API_URL , headers=headers,json=payload,timeout=30)
       hf_response.raise_for_status()

       # GESTION DE LA RÉPONSE INVALIDE
       try :
          result = hf_response.json()
       except ValueError:
            print("Erreur : L'API n'a pas renvoyé un JSON valide(Reponse Invalide).")
            return None
       

       if isinstance(result, list):
           result = result[0]
       top_label = result["label"]
       top_score = result["score"]
       
       top_score = round(result["score"]* 100, 2)
        # GESTION DES SCORES FAIBLES
       if top_score < 20:
          raise HTTPException(
            status_code=400,
            detail=f"Score faible ({top_score}%). Veuillez enrichir votre texte pour assurer une catégorisation précise, étape essentielle pour produire un résumé de qualité."
        )

       return { 
           
        "categorie": top_label,
        "score" : top_score

              }
    #  BLOCS D'EXCEPTIONS 
    except requests.exceptions.Timeout :
         raise HTTPException(status_code=504, detail="Hugging Face ne répond pas.")
    except requests.exceptions.ConnectionError :
         raise HTTPException(status_code=502, detail="Impossible de se connecter au service Hugging Face (Erreur Réseau).")
    except HTTPException as he:
        # On relance les exceptions HTTP créées manuellement (comme celle du score faible)
        raise he
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur : {str(e)}")
    
    







if __name__ == "__main__":
    labels = ["Finance", "RH", "IT", "Opérations","Marketing","Commerce"]
    text = "Nous devons renforcer la sécurité du serveur et améliorer le cloud."
    result = ZS_Classify(text,labels)
    categorie=result["categorie"]
    score = result["score"]
    print(categorie)
    print(score)
    print(result)

