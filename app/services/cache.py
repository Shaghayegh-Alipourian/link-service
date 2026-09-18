import asyncio

from redis.asyncio import Redis

from app.core.exceptions import CacheError


class CacheService:
    def __init__(
        self,
        redis: Redis,
        timeout: float = 1.0,
    ) -> None:
        self.redis = redis
        self.timeout = timeout

    async def get(self, key: str) -> str | None:
        try:
            value = await asyncio.wait_for(
                 self.redis.get(key),
                 timeout=self.timeout,
            )
            return value.decode() if isinstance(value, bytes) else value
        except TimeoutError as exc:
            raise CacheError(
                f"Cache GET timed out: {key}"
            ) from exc
        except Exception as exc:
            raise CacheError(
                f"Cache GET failed: {key}"
            ) from exc

    async def set(
        self,
        key: str,
        value: str,
        ttl: int | None = None,
    ) -> None:
        try:
            if ttl is None:
                await asyncio.wait_for(
                    self.redis.set(key, value),
                    timeout=self.timeout,
                )
            else:
                await asyncio.wait_for(
                    self.redis.set(
                        key,
                        value,
                        ex=ttl,
                    ),
                    timeout=self.timeout,
                )
        except TimeoutError as exc:
            raise CacheError(
                f"Cache SET timed out: {key}"
            ) from exc
        except Exception as exc:
            raise CacheError(
                f"Cache SET failed: {key}"
            ) from exc

    async def delete(self, key: str) -> None:
        try:
            await asyncio.wait_for(
                self.redis.delete(key),
                timeout=self.timeout,
            )
        except TimeoutError as exc:
            raise CacheError(
                f"Cache DELETE timed out: {key}"
            ) from exc
        except Exception as exc:
            raise CacheError(
                f"Cache DELETE failed: {key}"
            ) from exc

    async def increment(
        self,
        key: str,
        ttl: int | None = None,
    ) -> int:
        try:
            value = await asyncio.wait_for(
                self.redis.incr(key),
                timeout=self.timeout,
            )

            if value == 1 and ttl is not None:
                await asyncio.wait_for(
                    self.redis.expire(key, ttl),
                    timeout=self.timeout,
                )

            return value

        except TimeoutError as exc:
            raise CacheError(
                f"Cache INCREMENT timed out: {key}"
            ) from exc
        except Exception as exc:
            raise CacheError(
                f"Cache INCREMENT failed: {key}"
            ) from exc