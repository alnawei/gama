from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from core.config import settings

# 初始化异步引擎
engine = create_async_engine(settings.DATABASE_URL, echo=False)

# 声明异步 Session 制造工厂
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
