from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from redis.asyncio import Redis

class RateLimitMiddleware(BaseMiddleware):
    """
    通过 Redis 实现简单的用户消息防连点限流拦截器
    """
    def __init__(self, redis: Redis, limit_seconds: int = 2):
        self.redis = redis
        self.limit = limit_seconds
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)

        # 获取当前触发用户的 ID
        user_id = event.from_user.id
        redis_key = f"rate_limit:{user_id}"

        # 检查 Redis 键是否存在，若存在说明正在限制频段
        is_exists = await self.redis.get(redis_key)
        if is_exists:
            # 也可以不回复任何内容以降低资源开销
            return await event.answer("⚠️ 操作过于频繁，请稍候再试。")

        # 写入 Redis 并配置失效秒数
        await self.redis.set(redis_key, 1, ex=self.limit)
        return await handler(event, data)
