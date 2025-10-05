from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Header
from fastapi.responses import FileResponse
import aiofiles, os
from app.services.recordings_service import RecordingsService
from app.config import REDIS_URL
router = APIRouter(prefix='/api', tags=['recordings'])
svc = RecordingsService(redis_url=REDIS_URL)

@router.post('/video/recordings')
async def upload_recording(file: UploadFile = File(...), roomId: str = None, authorization: str = Header(None)):
    # read bytes
    content = await file.read()
    uploaded_by = None
    if authorization and authorization.startswith('Bearer '):
        uploaded_by = authorization.split(' ',1)[1][:20]
    metadata = await svc.save_file(content, file.filename, roomId, uploaded_by)
    return metadata

@router.get('/recordings')
async def list_recordings():
    return {'recordings': await svc.list_recordings()}

@router.get('/recordings/{filename}')
async def get_recording(filename: str):
    path = await svc.get_recording_path(filename)
    if not path:
        raise HTTPException(status_code=404, detail='Recording not found')
    return FileResponse(path)
