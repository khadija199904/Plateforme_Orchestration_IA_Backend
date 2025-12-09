def gemini_summary(prompt):
    
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt,config={
        "response_mime_type": "application/json",
        "response_json_schema": OutputGemini.model_json_schema(),
    },)
    result = OutputGemini.model_validate_json(response.text_resume)
    
    print(result)
    return
def gemini_summary(prompt):
    
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt,config={
        "response_mime_type": "application/json",
        "response_json_schema": OutputGemini.model_json_schema(),
    },)
    print(response.text)
    return



def build_prompt(text: str, categorie: str):
    return f"""
Voici un texte classé dans la catégorie : "{categorie}".

Texte : 
"{text}"


Ta mission :

- Rédiger un résumé d'une seule phrase de 20 mots maximum sur un ton simple
- Détecte le ton général du text : positif, neutre ou negatif.

"""

# def gemini_summary(prompt):
    
#     response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt,config={
#         "response_mime_type": "application/json",
#         "response_json_schema": OutputGemini.model_json_schema(),
#     },)
#     res = response.parsed
#     resume = res["text_resume"]
#     ton = res["ton"]
#     print(resume,ton)
#     return resume,ton 
#     # return OutputGemini(text_resume=resume,ton=ton)