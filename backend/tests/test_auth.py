from fastapi.testclient import TestClient
from backend.apps.services.main import app_asgi


client = TestClient(app_asgi)

def test_login_success():
    r = client.post('/api/auth/login', json={'username':'demo','password':'demo'})
    assert r.status_code == 200
    data = r.json()
    assert 'access_token' in data

def test_login_fail():
    r = client.post('/api/auth/login', json={'username':'x','password':'y'})
    assert r.status_code == 401
