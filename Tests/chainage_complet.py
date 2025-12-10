from api_app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_mok_analyse(mocker):
    fake_response = {
        'categorie': 'Cloud', 
        'score': 17.71, 
        'resume': 'Nous devons renforcer la sécurité du serveur et améliorer le cloud.', 
        'ton': 'négative'}
    
    mocker.patch("main.analyze_text", return_value= fake_response)

    resp = client.post("/analyse")

    assert resp.status_code == 200
    assert  resp.json() == [{
        'categorie': 'Cloud', 
        'score': 80, 
        'resume': 'Nous devons renforcer la sécurité du serveur et améliorer le cloud.', 
        'ton': 'négative'}]