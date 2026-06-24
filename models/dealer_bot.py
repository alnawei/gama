from sqlalchemy import BigInteger, String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base

class DealerBot(Base):
    __tablename__ = "dealer_bots"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    bot_token: Mapped[str] = mapped_column(String(255), unique=True, comment="机器人 API Token")
    group_id: Mapped[int] = mapped_column(BigInteger, nullable=True, comment="负责绑定的目标群组 ID")
    status: Mapped[str] = mapped_column(String(20), default="active", comment="激活状态: active, inactive")
