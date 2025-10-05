from dotenv import load_dotenv
import os
load_dotenv()
PERSONA_FETCHER_URL = os.getenv('PERSONA_FETCHER_URL', 'https://persona-fetcher-api.up.railway.app/personas')
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
TURN_URL = os.getenv('TURN_URL', '').strip()
TURN_USERNAME = os.getenv('TURN_USERNAME', '').strip()
TURN_CREDENTIAL = os.getenv('TURN_CREDENTIAL', '').strip()
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8000))
RECORDINGS_DIR = os.getenv('RECORDINGS_DIR', 'recordings')
JWT_SECRET = os.getenv('JWT_SECRET', 'change-me-demo-secret')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRE_SECONDS = 3600
