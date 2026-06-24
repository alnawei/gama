from datetime import datetime
from sqlalchemy import BigInteger, Numeric, String, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base

class TransactionLog(Base):
    __tablename__ = "transaction_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True, comment="关联的用户自增 ID")
    type: Mapped[str] = mapped_column(String(20), comment="流水类型: deposit, withdraw, grab, send")
    amount: Mapped[float] = mapped_column(Numeric(18, 4), comment="变动金额")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), comment="发生时间")
