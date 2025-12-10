from google import genai
from dotenv import load_dotenv
import requests
from fastapi import HTTPException

from api_app.schemas.serv_gemini import GeminiResponse
from api_app.core.config import GEMINI_API_KEY



client = genai.Client(api_key=GEMINI_API_KEY)



def build_prompt(text,categ):
    return f"""
   Analyse le texte ci-dessous classé sous le label "{categ}" :
   pour déterminer sa tonalité (positive, neutre ou négative),
    puis rédige un résumé d'une seule phrase de 20 mots maximum sur un ton simple : "{text}"

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

    # text = "Nous devons renforcer la sécurité du serveur et améliorer le cloud."
    # text = "Notre dernière campagne sur les réseaux sociaux a généré une augmentation de 45% de l’engagement client en seulement deux semaines. Grâce à une stratégie basée sur le contenu vidéo court et des publications interactives, nous avons réussi à toucher une audience plus jeune et à renforcer la visibilité de la marque. Les retours sont globalement positifs et montrent que notre approche centrée sur l’utilisateur fonctionne."
    result = gemini_analysis(text=text,categorie="IT")
    print(result)
    # resume = result["text_resume"]
    # ton = result ["ton"]
    
    # print(f"le resume est : {resume}")
    # print(f"le ton est : {ton}")