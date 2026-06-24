from sqlalchemy import BigInteger, Numeric, String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base

class RedPacket(Base):
    __tablename__ = "red_packets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group_id: Mapped[int] = mapped_column(BigInteger, index=True, comment="发包的目标群组 ID")
    total_amount: Mapped[float] = mapped_column(Numeric(18, 4), comment="红包总金额")
    packet_count: Mapped[int] = mapped_column(Integer, comment="拆分包数")
    grabbed_count: Mapped[int] = mapped_column(Integer, default=0, comment="已抢包数")
    status: Mapped[str] = mapped_column(String(20), default="active", comment="状态: active, finished, expired")
