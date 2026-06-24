import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from sqlalchemy import select

from core.config import settings
from database.session import AsyncSessionLocal
from models.dealer_bot import DealerBot
from routers.wallet_router import wallet_router
from middlewares.rate_limit import RateLimitMiddleware

# 设定基础日志输出格式
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SystemRunner")

async def load_dynamic_dealer_bots() -> list[str]:
    """
    数据面：动态读取数据库中状态为激活的发包机器人 Token 列表
    """
    async with AsyncSessionLocal() as session:
        try:
            stmt = select(DealerBot.bot_token).where(DealerBot.status == "active")
            result = await session.execute(stmt)
            return list(result.scalars().all())
        except Exception as e:
            logger.error(f"Error querying active dealer bots from MySQL: {e}")
            return []

async def main():
    # 1. 初始化 Redis 连池与存储
    redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)
    storage = RedisStorage(redis)

    # 2. 创建核心 Dispatcher
    dp = Dispatcher(storage=storage)

    # 3. 挂载全局拦截器 (防连点限制器)
    dp.message.outer_middleware(RateLimitMiddleware(redis))

    # 4. 注册各端独立路由
    dp.include_router(wallet_router)
    # dp.include_router(admin_router)   # 超管路由 (待自行补齐)
    # dp.include_router(dealer_router)  # 游戏路由 (待自行补齐)

    # 5. 加载静态双机（钱包及超管）
    bots: list[Bot] = []
    
    if settings.WALLET_BOT_TOKEN:
        bots.append(Bot(token=settings.WALLET_BOT_TOKEN))
        logger.info("Wallet Bot loaded successfully.")
    else:
        logger.warning("WALLET_BOT_TOKEN was not configured in .env!")

    if settings.ADMIN_BOT_TOKEN:
        bots.append(Bot(token=settings.ADMIN_BOT_TOKEN))
        logger.info("Admin Bot loaded successfully.")
    else:
        logger.warning("ADMIN_BOT_TOKEN was not configured in .env!")

    # 6. 数据控制分离面：加载并拉起数据库中的动态发包机器人
    dealer_tokens = await load_dynamic_dealer_bots()
    for idx, token in enumerate(dealer_tokens, start=1):
        try:
            # 校验 token 合法性并追加到启动实例中
            bot_instance = Bot(token=token)
            bots.append(bot_instance)
            logger.info(f"Dynamic Dealer Bot #{idx} loaded (token preview: {token[:10]}...)")
        except Exception as err:
            logger.error(f"Failed to load Dynamic Bot #{idx}: {err}")

    if not bots:
        logger.error("No active bot instances detected. Exiting system.")
        return

    # 7. 并发拉起所有机器人轮询监听
    logger.info("Initializing bot federation and starting polling...")
    try:
        # aiogram 3.x 允许传入多个 bot 对象并行消费同一个路由池分发的事件
        await dp.start_polling(*bots)
    except Exception as run_err:
        logger.critical(f"Engine run error: {run_err}")
    finally:
        # 清理工作
        await redis.close()
        for bot in bots:
            await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
