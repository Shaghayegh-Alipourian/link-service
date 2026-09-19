from redis.asyncio import Redis

from app.core.config import settings
from app.core.exceptions import RateLimitExceededError

RATE_LIMIT_SCRIPT = """
local current = redis.call('INCR', KEYS[1])

if current == 1 then
    redis.call('EXPIRE', KEYS[1], ARGV[1])
end

return current
"""


class RateLimitService:
    def __init__(
        self,
        redis: Redis,
        limit: int | None = None,
        window: int | None = None,
    ) -> None:
        self.redis = redis
        self.limit = settings.rate_limit if limit is None else limit
        self.window = settings.rate_limit_window if window is None else window

    async def check(self, client_id: str) -> None:
        key = f"rate_limit:{client_id}"

        count = await self.redis.eval(
            RATE_LIMIT_SCRIPT,
            1,
            key,
            self.window,
        )

        if int(count) > self.limit:
            raise RateLimitExceededError(
                f"Rate limit exceeded: {self.limit} requests per {self.window} seconds."
            )
