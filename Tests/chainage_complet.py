import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from fastapi import FastAPI, Depends
from api_app.main import app ,verify_token 
# -------------------------------------------------------------
# client = TestClient(app)
@pytest.fixture
def client() : 
    return TestClient(app)
@pytest.fixture
def fake_verify_token():
    
    app.dependency_overrides[verify_token] = lambda: "fake_user"
    


def test_analyse_endpoint_success(client, fake_verify_token, mocker):
    
    payload = {"text": "Nous devons renforcer la sécurité du serveur."}

   # 2. Mock Hugging Face
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


def test_analyse_endpoint_auth_fail(client, mocker):
    """Vérifie que sans l'override d'auth, ça bloque (401 ou 403)"""
    
    # On n'utilise PAS la fixture override_auth ici
    # On s'assure qu'aucun override ne traîne
    app.dependency_overrides = {} 

    payload = {"text": "Test secret"}
    response = client.post("/analyse", json=payload)

    # Si ça renvoie 404 ici, c'est que l'URL "/analyse" est fausse dans @app.post(...)
    # Si ça renvoie 401/403, c'est bon (accès refusé)
    assert response.status_code in [401, 403, 422] 
    # Note: 422 arrive parfois si le token est attendu dans le body ou header manquant