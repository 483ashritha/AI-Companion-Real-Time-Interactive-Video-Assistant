import json, logging
from typing import Dict, Any, Optional
logger = logging.getLogger(__name__)
try:
    import redis.asyncio as aioredis
except Exception:
    aioredis = None

class RoomStore:
    def __init__(self, redis_url: str = ""):
        self.redis_url = redis_url
        self.redis = None
        self._in_memory = {}
        if redis_url and aioredis:
            try:
                self.redis = aioredis.from_url(redis_url, decode_responses=True)
                logger.info("RoomStore: connected to Redis")
            except Exception as e:
                logger.warning("RoomStore: Redis init failed: %s", e)
                self.redis = None

    async def save_room(self, room_id: str, room: Dict[str, Any]):
        if self.redis:
            try:
                await self.redis.hset("rooms", room_id, json.dumps(room))
                return
            except Exception as e:
                logger.warning("RoomStore.save_room redis error: %s", e)
        self._in_memory[room_id] = room

    async def get_room(self, room_id: str) -> Optional[Dict[str, Any]]:
        if self.redis:
            try:
                raw = await self.redis.hget("rooms", room_id)
                if raw:
                    return json.loads(raw)
            except Exception as e:
                logger.warning("RoomStore.get_room redis error: %s", e)
        return self._in_memory.get(room_id)

    async def list_rooms(self):
        if self.redis:
            try:
                raw = await self.redis.hgetall("rooms")
                return {k: json.loads(v) for k, v in raw.items()}
            except Exception as e:
                logger.warning("RoomStore.list_rooms redis error: %s", e)
        return self._in_memory.copy()
