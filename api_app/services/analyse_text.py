from .service_HF import ZS_Classify
from .service_Gemini import gemini_analysis

def analyse(text):
    
    labels = ["Finance","RH","IT","Opérations","Marketing","Commerce","Ventes","Service client","Relation client",
           "Communication","Stratégie","Management","Leadership","Recrutement","Formation","Développement personnel",
           "Innovation","Recherche","Développement produit","Qualité","Production","Logistique","Supply chain","Achats","Juridique",
           "Conformité","Audit","Comptabilité","Fiscalité","Trésorerie","Événementiel","Partenariat","Sponsoring","Publicité",
           "Branding","Réseaux sociaux","SEO","Contenu","Design","UX/UI","Data Science","Intelligence artificielle","Big Data",
            "Cloud","Sécurité", "Gestion de projet", "Agile","Scrum","Innovation digitale","Transformation digitale"]
    
    #  Hugging Face
    HF_result = ZS_Classify(text, labels)
    categorie = HF_result["categorie"]
    score = round(HF_result["score"] * 100, 2)
    
    #  Gemini
    Gemini_result = gemini_analysis(text, categorie)
    resume = Gemini_result["text_resume"]
    ton = Gemini_result["ton"]
    
    # Résultat global
    global_result = {
        "categorie": categorie,
        "score": score,
        "resume": resume,
        "ton": ton
    }
    
    return global_result




if __name__ == "__main__":
    
    text = "Nous devons renforcer la sécurité du serveur et améliorer le cloud."
    result = analyse(text)
    print(result)