import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from fastapi import HTTPException
import requests
import pytest
from unittest.mock import Mock,patch
from api_app.services.service_HF import ZS_Classify



@pytest.fixture
def mock_response(mocker):
    
    mock = mocker.patch("requests.post")
    mock.return_value.status_code = 200
    mock.raise_for_status.return_value = None
    return mock
def test_mock_HaggingFace (mock_response) :
 
    labels = ["Finance", "RH", "IT", "Opérations","Marketing","Commerce"]
    text = "Découvrez notre nouvelle solution conçue pour augmenter vos ventes et renforcer votre stratégie marketing. Grâce à une communication ciblée et un positionnement clair, vous attirez plus de clients et développez votre marque efficacement."
    
    mock_response.return_value.json.return_value = {
        'label': 'Marketing',
        'score': 0.8013417720794678
    }
    
    res = ZS_Classify(text,labels)
    assert res["categorie"] == "Marketing"
    assert res["score"] > 0.6


  # Test mock de service Geimini API Down 
def test_HF_Api_down(mock_response):
    mock_response.side_effect = requests.ConnectionError 
    
    with pytest.raises(HTTPException) as err:
        ZS_Classify("txt", ["IT"])
    assert err.value.status_code == 502
    