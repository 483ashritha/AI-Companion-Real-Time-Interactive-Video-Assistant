import os, json, uuid, logging
from typing import Dict, Any, List, Optional
from app.config import RECORDINGS_DIR, REDIS_URL

logger = logging.getLogger(__name__)
try:
    import redis.asyncio as aioredis
except Exception:
    aioredis = None

class RecordingsService:
    def __init__(self, redis_url: str = ""):
        self.redis_url = redis_url
        self.redis = None
        if redis_url and aioredis:
            try:
                self.redis = aioredis.from_url(redis_url, decode_responses=True)
                logger.info("RecordingsService: connected to Redis")
            except Exception as e:
                logger.warning("RecordingsService: Redis init failed: %s", e)
                self.redis = None
        os.makedirs(RECORDINGS_DIR, exist_ok=True)

    async def save_file(self, file_bytes: bytes, original_filename: str, room_id: str, uploaded_by: str = None) -> Dict[str, Any]:
        filename = f"{uuid.uuid4().hex}_{original_filename}"
        path = os.path.join(RECORDINGS_DIR, filename)
        with open(path, 'wb') as f:
            f.write(file_bytes)
        metadata = {"recordingId": filename, "roomId": room_id, "uploadedBy": uploaded_by, "size": os.path.getsize(path)}
        # store metadata in redis list
        try:
            if self.redis:
                await self.redis.hset('recordings', filename, json.dumps(metadata))
        except Exception as e:
            logger.warning("Failed to store metadata in redis: %s", e)
        return metadata

    async def list_recordings(self) -> List[Dict[str, Any]]:
        results = []
        try:
            if self.redis:
                raw = await self.redis.hgetall('recordings')
                for k,v in raw.items():
                    results.append(json.loads(v))
                return results
        except Exception as e:
            logger.warning("RecordingsService.list_recordings redis error: %s", e)
        # fallback: list files in folder
        for fname in os.listdir(RECORDINGS_DIR):
            fpath = os.path.join(RECORDINGS_DIR, fname)
            if os.path.isfile(fpath):
                results.append({"recordingId": fname, "url": f"/api/recordings/{fname}", "size": os.path.getsize(fpath)})
        return results

    async def get_recording_path(self, filename: str) -> Optional[str]:
        path = os.path.join(RECORDINGS_DIR, filename)
        if os.path.exists(path):
            return path
        return None
