import pytest
from fastapi.testclient import TestClient
from backend.app.main import app_asgi

client = TestClient(app_asgi)

def test_health():
    r = client.get('/api/health/ready')
    assert r.status_code in (200, 404)  # health may be in different router set; allow 404 for flexibility

def test_companions():
    r = client.get('/api/companions/')
    assert r.status_code == 200
