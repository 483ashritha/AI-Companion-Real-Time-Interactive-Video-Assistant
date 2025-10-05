from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt
from app.config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_SECONDS

router = APIRouter(prefix='/api/auth', tags=['auth'])

class LoginRequest(BaseModel):
    username: str
    password: str

# Very small demo auth. In real systems, check DB or external auth.
@router.post('/login')
async def login(req: LoginRequest):
    if req.username == 'demo' and req.password == 'demo':
        expire = datetime.utcnow() + timedelta(seconds=JWT_EXPIRE_SECONDS)
        token = jwt.encode({'sub': req.username, 'exp': expire.timestamp()}, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return {'access_token': token, 'token_type': 'bearer'}
    raise HTTPException(status_code=401, detail='Invalid credentials')

def verify_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload.get('sub')
    except Exception:
        return None

def get_current_user(token: str = Depends(lambda: None)):
    # placeholder dependency; real usage would extract Authorization header
    return None
