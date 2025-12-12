from google import genai
from dotenv import load_dotenv
import requests
from fastapi import HTTPException

from ..schemas.serv_gemini import GeminiResponse
from ..core.config import GEMINI_API_KEY



client = genai.Client(api_key=GEMINI_API_KEY)



def build_prompt(text,categ):
    return f"""
         Rôle : Tu es un assistant expert en synthèsecontenu.

         Consigne :
         Analyse le texte ci-dessous classé sous le label "{categ}".
         1. Détermine sa tonalité (positive, neutre ou négative).
         2. Rédige un résumé de trois phrases maximum et de 40 mots maximum sur un ton simple.

        Texte :
        '''
        {text}
        '''

         """

def gemini_analysis(text,categorie):

  prompt = build_prompt(text,categorie)
  try :
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt,config={
        "response_mime_type": "application/json",
        "response_json_schema": GeminiResponse.model_json_schema(),
    },)
    # Getsion de reponse mal formée
    if not response.parsed:
        raise ValueError("Réponse Gemini mal formée")
    res = response.parsed
    resume = res["text_resume"]
    ton = res["ton"]
    
    return { 
        "text_resume" : resume,
        "ton" : ton
        }
  # Gestion API down
  except requests.ConnectionError:
        raise HTTPException(status_code=503, detail="Impossible de se connecter à Gemini")
  





















if __name__ == "__main__":
    text = "Découvrez notre nouvelle solution conçue pour augmenter vos ventes et renforcer votre stratégie marketing. Grâce à une communication ciblée et un positionnement clair, vous attirez plus de clients et développez votre marque efficacement."
    result = gemini_analysis(text=text,categorie="Marketing")
    print(result)
   