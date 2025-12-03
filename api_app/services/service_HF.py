import os
import requests
from dotenv import load_dotenv
from fastapi import HTTPException


load_dotenv()

HF_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")


if not HF_API_TOKEN:
    raise ValueError("La clé d'API Hugging Face n'est pas définie. Veuillez la mettre dans le fichier .env")
headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"

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
    hf_response = requests.post(API_URL , headers=headers,json=payload,timeout=30)
         
    result = hf_response.json()
    
    if isinstance(result, list):
        result = result[0]
    
    top_label = result["label"]
    top_score = result["score"]
    
    return { 
        "categorie": top_label,
        "score" : top_score
            }


if __name__ == "__main__":
    labels = ["Finance", "RH", "IT", "Opérations","Marketing","Commerce",]
    # text = "Nous devons renforcer la sécurité du serveur et améliorer le cloud."
    text = "Notre dernière campagne sur les réseaux sociaux a généré une augmentation de 45% de l’engagement client en seulement deux semaines. Grâce à une stratégie basée sur le contenu vidéo court et des publications interactives, nous avons réussi à toucher une audience plus jeune et à renforcer la visibilité de la marque. Les retours sont globalement positifs et montrent que notre approche centrée sur l’utilisateur fonctionne."
    result = ZS_Classify(text,labels)
    categorie=result["categorie"]
    score = result["score"]
    print(categorie)
    print(score)

