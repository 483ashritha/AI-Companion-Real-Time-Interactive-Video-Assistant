from fastapi import APIRouter
from fastapi.responses import JSONResponse
import httpx, logging
from app.config import PERSONA_FETCHER_URL
router = APIRouter(prefix='/api/companions', tags=['companions'])
logger = logging.getLogger(__name__)

@router.get('/')
async def get_companions():
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(PERSONA_FETCHER_URL, timeout=8.0)
            r.raise_for_status()
            return JSONResponse(status_code=r.status_code, content=r.json())
    except Exception as e:
        logger.warning('Failed to fetch companions: %s', e)
        fallback = [
            {'id': 'comp-1', 'name': 'Ava', 'avatar': 'https://i.pravatar.cc/150?img=1', 'voiceId': 'voice-1'},
            {'id': 'comp-2', 'name': 'Kai', 'avatar': 'https://i.pravatar.cc/150?img=2', 'voiceId': 'voice-2'}
        ]
        return {'data': fallback, 'warning': str(e)}
