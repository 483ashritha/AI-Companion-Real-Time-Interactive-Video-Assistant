Backend README

- Create virtualenv, install requirements.txt
- Set .env (copy .env.example)
- Run: uvicorn app.main:app_asgi --reload --port 8000
- Endpoints:
  - /api/companions/
  - /api/video/rooms/
  - /api/video/recordings (POST to upload)
  - /api/recordings (GET list)
  - /api/auth/login (POST username=demo,password=demo)
