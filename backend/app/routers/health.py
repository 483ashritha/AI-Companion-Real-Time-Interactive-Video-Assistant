from fastapi import APIRouter
router = APIRouter(prefix='/api/health', tags=['health'])
@router.get('/ready')
async def ready():
    return {'status':'ok','service':'ai-companion-backend'}
