import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from api_app.core.security import verify_token

from api_app.main import app 



@pytest.fixture
def client() : 
    return TestClient(app)


@pytest.fixture
def fake_verify_token():
    
    app.dependency_overrides[verify_token] = lambda: "fake_user"
    


def test_analyse_endpoint_success(client, fake_verify_token, mocker):
    
    payload = {"text": "Nous devons renforcer la sécurité du serveur."}

   #  Mock Hugging Face
    mock_hf = mocker.patch("api_app.services.analyse_text.ZS_Classify")
    mock_hf.return_value = {"categorie": "IT", "score": 0.9512}

    # Mock Gemini
    mock_gemini = mocker.patch("api_app.services.analyse_text.gemini_analysis")
    mock_gemini.return_value = {"text_resume": "Résumé test", "ton": "neutre"}

    # Appel (POST /analyse)
    response = client.post("/analyse", json=payload)

    
    assert response.status_code == 200
    data = response.json()
    assert data["categorie"] == "IT"
    assert data["score"] == 95.12


def test_analyse_auth_fail(client, mocker):
    
    app.dependency_overrides = {} 

    payload = {"text": "Test secret"}
    response = client.post("/analyse", json=payload)

    # 401 (Token faux) ou 422 (Token absent/Header manquant)
    assert response.status_code in [401, 422]
    