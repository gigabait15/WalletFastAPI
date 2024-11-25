from sqlalchemy import String, DateTime, Column, Integer, Boolean, func
from database import Base


class Wallets(Base):
    """
    Класс для формирования таблицы в БД
    """
    UUID = Column(String(36), primary_key=True, unique=True, nullable=False)
    balance = Column(Integer, default=0, nullable=False)
    deposit = Column(Boolean, nullable=False, default=False)
    withdraw = Column(Boolean, nullable=False, default=False)
    date_operations = Column(DateTime, server_default=func.now(), nullable=False)

    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.UUID})"


