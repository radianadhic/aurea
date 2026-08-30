"""Redis cache manager."""
import json
from typing import Any, Optional

import redis.asyncio as redis
import structlog
from app.core.config import settings

logger = structlog.get_logger()


class CacheManager:
    def __init__(self) -> None:
        self._client: Optional[redis.Redis] = None

    async def connect(self) -> None:
        try:
            self._client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
                db=settings.REDIS_DB,
                decode_responses=True,
                socket_connect_timeout=5,
            )
            await self._client.ping()
            logger.info("cache.connected", host=settings.REDIS_HOST, port=settings.REDIS_PORT)
        except Exception as e:
            logger.warning("cache.connect_failed", error=str(e))
            self._client = None

    async def disconnect(self) -> None:
        if self._client:
            await self._client.close()
            self._client = None

    async def get(self, key: str) -> Optional[Any]:
        if not self._client:
            return None
        try:
            value = await self._client.get(key)
            return json.loads(value) if value else None
        except Exception as e:
            logger.warning("cache.get_failed", key=key, error=str(e))
            return None

    async def set(self, key: str, value: Any, ttl: int | None = None) -> bool:
        if not self._client:
            return False
        try:
            ttl = ttl or settings.CACHE_TTL
            return bool(await self._client.set(key, json.dumps(value, default=str), ex=ttl))
        except Exception as e:
            logger.warning("cache.set_failed", key=key, error=str(e))
            return False

    async def delete(self, key: str) -> bool:
        if not self._client:
            return False
        try:
            return bool(await self._client.delete(key))
        except Exception as e:
            logger.warning("cache.delete_failed", key=key, error=str(e))
            return False


cache_manager = CacheManager()
