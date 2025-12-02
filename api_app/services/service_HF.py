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
    translated_text = result[0]['translation_text']
    return translated_text