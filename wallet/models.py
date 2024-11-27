from sqlalchemy import String, Column, Integer
from database import Base


class Wallet(Base):
    """
    Модель для представления кошелька.

    Атрибуты:
        uuid: Уникальный идентификатор кошелька.
        balance: Баланс кошелька в целых числах.
    """
    UUID = Column(String, primary_key=True, index=True)
    balance = Column(Integer, default=0)

    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.UUID})"
