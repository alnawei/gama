import asyncio
import logging
import os
import sys
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

# 加载 .env 环境变量
load_dotenv()

# 设置系统日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("MultiBotEngine")

# =====================================================================
# 1. 模拟导入外部业务路由 (Routers)
# =====================================================================
# 实际生产环境中，请取消下方三行的注释以导入您 routers 目录下的真实路由文件：
# from routers.wallet_router import wallet_router
# from routers.admin_router import admin_router
# from routers.dealer_router import dealer_router

from aiogram import Router
# 此处使用 Mock 路由对象仅用于保证此主程序可直接运行，实际开发时请替换为真实路由
wallet_router = Router(name="wallet_router")
admin_router = Router(name="admin_router")
dealer_router = Router(name="dealer_router")


async def main():
    logger.info("Initializing multi-bot physical isolation system...")

    # =====================================================================
    # 2. 多 Dispatcher 隔离设计
    # =====================================================================
    # static_dp：负责私聊静态机器人组（财务中心与超管控制台）
    # 共享相同的存储器、过滤器上下文或中间件，但与群组内的游戏逻辑物理隔离
    static_dp = Dispatcher()

    # dealer_dp：预留给群组内的动态发包机器人（游戏数据面）
    # 确保高频抢包、炸弹计算等业务不阻塞财务机器人的正常响应
    dealer_dp = Dispatcher()

    # =====================================================================
    # 3. 路由 (Routers) 精确挂载
    # =====================================================================
    # 将钱包和超管控制台挂载至静态调度器
    static_dp.include_router(wallet_router)
    static_dp.include_router(admin_router)
    logger.info("Successfully mounted [wallet_router] and [admin_router] to static_dp.")

    # 将游戏发包处理挂载至发包调度器 (预留)
    dealer_dp.include_router(dealer_router)
    logger.info("Successfully mounted [dealer_router] to dealer_dp.")

    # =====================================================================
    # 4. Bot 实例初始化 (读取环境变量)
    # =====================================================================
    wallet_token = os.getenv("WALLET_BOT_TOKEN")
    admin_token = os.getenv("ADMIN_BOT_TOKEN")

    if not wallet_token or not admin_token:
        logger.error("Missing WALLET_BOT_TOKEN or ADMIN_BOT_TOKEN in environment variables.")
        sys.exit(1)

    wallet_bot = Bot(token=wallet_token)
    admin_bot = Bot(token=admin_token)

    # =====================================================================
    # 5. 异步并发启动与物理隔离运行 (核心并发机制)
    # =====================================================================
    logger.info("Polling configuration is ready. Starting concurrent execution loop...")

    # 并发启动说明：
    # 1. 在 aiogram 3.x 中，单一 Dispatcher 支持传入多个 Bot 实例（即 multibot 模式）。
    #    通过 `static_dp.start_polling(wallet_bot, admin_bot)`，静态调度器将同时为这两个机器人拉取更新。
    # 2. 我们通过 `asyncio.gather` 将“静态调度器任务”与“未来可能运行的游戏调度器任务”并发挂起。
    #    这样可以实现不同 Dispatcher 实例在物理线程（协程空间）中的完全隔离运行。
    try:
        await asyncio.gather(
            # 任务 A: 启动静态控制面机器人们的轮询 (Wallet Bot + Admin Bot 并行)
            static_dp.start_polling(wallet_bot, admin_bot, skip_updates=True),
            
            # 任务 B: 预留给后续动态发包机器人调度器 (dealer_dp) 的轮询任务
            # 待后续您通过数据库读出并实例化 dealer_bot 之后，只需在此处解除注释并传入 dealer_bot 即可
            # dealer_dp.start_polling(dealer_bot, skip_updates=True)
        )
    except Exception as e:
        logger.error(f"An unexpected error occurred during polling: {e}")
    finally:
        # 优雅关闭：确保系统退出时安全释放 HTTP 客户端会话资源
        await wallet_bot.session.close()
        await admin_bot.session.close()
        logger.info("All bot sessions have been securely closed.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("System process terminated manually.")
