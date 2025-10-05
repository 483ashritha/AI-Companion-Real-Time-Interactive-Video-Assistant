from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import uuid
from app.services.room_store import RoomStore
from app.config import REDIS_URL

router = APIRouter(prefix='/api/video/rooms', tags=['rooms'])
store = RoomStore(redis_url=REDIS_URL)

@router.post('/')
async def create_room(payload: Dict[str, Any]):
    room_id = str(uuid.uuid4())[:8]
    room = {'roomId': room_id, 'companionId': payload.get('companionId'), 'userId': payload.get('userId'), 'status': 'active', 'expiresAt': None}
    await store.save_room(room_id, room)
    return room

@router.get('/{room_id}')
async def get_room(room_id: str):
    room = await store.get_room(room_id)
    if not room:
        raise HTTPException(status_code=404, detail='Room not found')
    return room
