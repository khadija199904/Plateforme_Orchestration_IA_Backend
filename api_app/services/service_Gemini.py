from google import genai
from dotenv import load_dotenv
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from schemas.Output_SR_gemini import OutputGemini





load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KE")


client = genai.Client(api_key=GEMINI_API_KEY)



def build_prompt(text: str, categ: str):
    return f"""
   Analyse le texte ci-dessous classé sous le label "{categ}" :
   pour déterminer sa tonalité (positive, neutre ou négative),
    puis rédige un résumé d'une seule phrase de 20 mots maximum sur un ton simple : "{text}"

     """

def gemini_analysis(text,categorie):

    prompt = build_prompt(text,categorie)
    
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt,config={
        "response_mime_type": "application/json",
        "response_json_schema": OutputGemini.model_json_schema(),
    },)
    res = response.parsed
    resume = res["text_resume"]
    ton = res["ton"]
  
    return { 
        "text_resume" : resume,
        "ton" : ton
        }






















if __name__ == "__main__":
    # text = "Nous devons renforcer la sécurité du serveur et améliorer le cloud."
    text = "Notre dernière campagne sur les réseaux sociaux a généré une augmentation de 45% de l’engagement client en seulement deux semaines. Grâce à une stratégie basée sur le contenu vidéo court et des publications interactives, nous avons réussi à toucher une audience plus jeune et à renforcer la visibilité de la marque. Les retours sont globalement positifs et montrent que notre approche centrée sur l’utilisateur fonctionne."
    result = gemini_analysis(text=text,categorie="IT")
    resume = result["text_resume"]
    ton = result ["ton"]
    print(f"le resume est : {resume}")
    print(f"le ton est : {ton}")