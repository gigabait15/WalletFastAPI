from pydantic import BaseModel, Field


class WalletCreate(BaseModel):
    """
    Схема для создания нового кошелька.

    Атрибуты:
        initial_balance: Начальный баланс кошелька (по умолчанию 0).
    """
    initial_balance: int = Field(0, ge=0)


class WalletOperation(BaseModel):
    """
    Схема для операции с кошельком.

    Атрибуты:
        operationType: Тип операции (DEPOSIT или WITHDRAW).
        amount: Сумма операции (должна быть положительной).
    """
    operationType: str = Field(..., pattern="^(DEPOSIT|WITHDRAW)$")
    amount: int = Field(..., gt=0)


class WalletResponse(BaseModel):
    """
    Схема для ответа с балансом кошелька.

    Атрибуты:
        uuid: Уникальный идентификатор кошелька.
        balance: Баланс кошелька.
    """
    UUID: str
    balance: int
