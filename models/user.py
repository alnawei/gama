from sqlalchemy.orm import DeclarativeBase, declared_attr

class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls) -> str:
        # 默认使用类名小写作为表名
        return cls.__name__.lower() + "s"
