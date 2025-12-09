import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


import requests
import pytest
from fastapi import HTTPException
from unittest.mock import Mock,patch
from api_app.services.service_Gemini import gemini_analysis

def test_gemini_success (mocker):
    categorie = "Marketing"
    text = "Découvrez notre nouvelle solution conçue pour augmenter vos ventes et renforcer votre stratégie marketing. Grâce à une communication ciblée et un positionnement clair, vous attirez plus de clients et développez votre marque efficacement."

    fake_response = Mock()
    fake_response.status_code = 200
    
    fake_response.parsed = {
        "text_resume": 'Découvrez notre solution qui augmente vos ventes, attire les clients '
        'et renforce efficacement votre marketing.',
        "ton": 'positive'
        }
    
    mocker.patch("api_app.services.service_Gemini.client.models.generate_content", return_value=fake_response) 
    resultat = gemini_analysis(text,categorie)


    assert resultat["text_resume"] == (
        'Découvrez notre solution qui augmente vos ventes, attire les clients '
        'et renforce efficacement votre marketing.'
    )
    assert resultat["ton"] == "positive"


   
   
  # Test mock de service Geimini API Down 
def test_Gemini_Api_down(mocker):
    mocker.patch("api_app.services.service_Gemini.client.models.generate_content", 
                 side_effect=requests.ConnectionError
                 ) 
    
    with pytest.raises(HTTPException) as err:
        gemini_analysis("txt", "IT")
    
    assert err.value.status_code == 503 
# test de service Gemini (reponse mal formé)

def test_gemini_malformed(mocker):

    fake_response = Mock()
    fake_response.parsed = None

    mocker.patch("api_app.services.service_Gemini.client.models.generate_content", 
                 return_value = fake_response
                 ) 
    with pytest.raises(ValueError) as err:
        gemini_analysis("txt", "IT")
    
    