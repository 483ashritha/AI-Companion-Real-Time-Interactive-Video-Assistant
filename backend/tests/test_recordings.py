import io
from fastapi.testclient import TestClient
from main import app_asgi


client = TestClient(app_asgi)

def test_upload_and_list_recording():
    data = {'roomId':'testroom'}
    files = {'file': ('test.webm', b'testdata', 'video/webm')}
    r = client.post('/api/video/recordings', files=files, data=data)
    assert r.status_code == 200
    j = r.json()
    assert 'recordingId' in j
    # list
    r2 = client.get('/api/recordings')
    assert r2.status_code == 200
    assert 'recordings' in r2.json()
