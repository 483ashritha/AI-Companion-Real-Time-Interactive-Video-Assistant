import logging, socketio
from app.config import REDIS_URL
try:
    import redis.asyncio as aioredis
except Exception:
    aioredis = None
logger = logging.getLogger(__name__)
sio_manager = socketio.AsyncRedisManager(REDIS_URL) if (REDIS_URL and aioredis) else None
sio = socketio.AsyncServer(async_mode='asgi', client_manager=sio_manager, cors_allowed_origins='*')

@sio.event
async def connect(sid, environ):
    logger.info('Socket connected: %s', sid)

@sio.event
async def disconnect(sid):
    logger.info('Socket disconnected: %s', sid)

@sio.event
async def join(sid, data):
    room_id = data.get('roomId'); user_id = data.get('userId')
    if not room_id or not user_id:
        await sio.emit('error', {'msg':'join requires roomId & userId'}, to=sid); return
    await sio.save_session(sid, {'roomId': room_id, 'userId': user_id})
    await sio.enter_room(sid, room_id)
    await sio.emit('join', {'roomId': room_id, 'userId': user_id}, room=room_id, skip_sid=sid)
    logger.info('User %s joined room %s', user_id, room_id)

@sio.event
async def leave(sid, data):
    room_id = data.get('roomId'); user_id = data.get('userId')
    await sio.leave_room(sid, room_id); await sio.emit('leave', {'roomId': room_id, 'userId': user_id}, room=room_id)

@sio.event
async def offer(sid, data):
    room_id = data.get('roomId'); await sio.emit('offer', data, room=room_id, skip_sid=sid)

@sio.event
async def answer(sid, data):
    room_id = data.get('roomId'); await sio.emit('answer', data, room=room_id, skip_sid=sid)

@sio.event
async def candidate(sid, data):
    room_id = data.get('roomId'); await sio.emit('candidate', data, room=room_id, skip_sid=sid)

@sio.event
async def chat(sid, data):
    room_id = data.get('roomId'); await sio.emit('chat', data, room=room_id)
