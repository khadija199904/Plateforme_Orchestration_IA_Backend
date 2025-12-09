import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from fastapi import HTTPException
import requests
import pytest
from unittest.mock import Mock,patch
from api_app.services.service_HF import ZS_Classify

def test_mock_HaggingFace (mocker) :
 
    labels = ["Finance", "RH", "IT", "Opérations","Marketing","Commerce"]
    text = "Découvrez notre nouvelle solution conçue pour augmenter vos ventes et renforcer votre stratégie marketing. Grâce à une communication ciblée et un positionnement clair, vous attirez plus de clients et développez votre marque efficacement."
    
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
              'label': 'Marketing',
              'score': 0.8013417720794678
              }
    mocker.patch()
    mocker.patch("requests.post",return_value = mock_response)

    res = ZS_Classify(text,labels)
    assert res["categorie"] == "Marketing"
    assert res["score"] > 0.6


  # Test mock de service Geimini API Down 
def test_HF_Api_down(mocker):
    mocker.patch("requests.post", 
                 side_effect=requests.ConnectionError
                 ) 
    
    with pytest.raises(HTTPException) as err:
        ZS_Classify("txt", ["IT"])