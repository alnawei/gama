import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    WALLET_BOT_TOKEN: str = os.getenv("WALLET_BOT_TOKEN", "")
    ADMIN_BOT_TOKEN: str = os.getenv("ADMIN_BOT_TOKEN", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+aiomysql://root:root@localhost:3306/game_db")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

settings = Config()
