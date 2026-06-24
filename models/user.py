from sqlalchemy import BigInteger, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_user_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, comment="Telegram 唯一 ID")
    balance: Mapped[float] = mapped_column(Numeric(18, 4), default=0.0000, comment="可用余额")
    frozen_balance: Mapped[float] = mapped_column(Numeric(18, 4), default=0.0000, comment="游戏冻结金额")
    status: Mapped[str] = mapped_column(String(20), default="active", comment="状态: active, banned")
