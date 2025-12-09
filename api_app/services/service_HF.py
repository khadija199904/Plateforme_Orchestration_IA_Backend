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

    payload = {
        "inputs": text,
        "parameters": {
            "candidate_labels": labels
        }
       }

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
       
    #    # GESTION DES SCORES FAIBLES
    #    seuil = 0.6 
    #    if top_score < seuil :
    #        top_label = "Catégorie Inconnu"
    #    else : 
    #      top_label = top_label


       return { 
           
        "categorie": top_label,
        "score" : top_score

              }
    #  BLOCS D'EXCEPTIONS 
    except requests.exceptions.Timeout :
         raise HTTPException(status_code=504, detail="Hugging Face ne répond pas (Timeout).")
    except requests.exceptions.ConnectionError :
         raise HTTPException(status_code=502, detail="Impossible de se connecter au service Hugging Face (Erreur Réseau).")
    except Exception as e:
         raise HTTPException(status_code=500, detail=f"Erreur interne du serveur : {e}")
    







if __name__ == "__main__":
    labels = ["Finance", "RH", "IT", "Opérations","Marketing","Commerce"]
    text = "Découvrez notre nouvelle solution conçue pour augmenter vos ventes et renforcer votre stratégie marketing. Grâce à une communication ciblée et un positionnement clair, vous attirez plus de clients et développez votre marque efficacement."
    # text = "Nous devons renforcer la sécurité du serveur et améliorer le cloud."
    # text = "Notre dernière campagne sur les réseaux sociaux a généré une augmentation de 45% de l’engagement client en seulement deux semaines. Grâce à une stratégie basée sur le contenu vidéo court et des publications interactives, nous avons réussi à toucher une audience plus jeune et à renforcer la visibilité de la marque. Les retours sont globalement positifs et montrent que notre approche centrée sur l’utilisateur fonctionne."
    result = ZS_Classify(text,labels)
    categorie=result["categorie"]
    score = result["score"]
    print(categorie)
    print(score)
    print(result)

