from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from wallet.models import Wallet
import logging

logger = logging.getLogger(__name__)


async def get_wallet_balance(session: AsyncSession, wallet_uuid: str) -> int:
    """
    Получает текущий баланс кошелька.

    :param session: Сессия базы данных.
    :param wallet_uuid: UUID кошелька.
    :return: Баланс кошелька.
    :raises HTTPException: Если кошелек не найден.
    """
    result = await session.execute(select(Wallet).where(Wallet.UUID == wallet_uuid))
    wallet = result.scalars().first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet.balance


async def perform_wallet_operation(session: AsyncSession, wallet_uuid: str, operation: str, amount: int):
    """
    Выполняет операцию над кошельком (пополнение или списание).

    :param session: Сессия базы данных.
    :param wallet_uuid: UUID кошелька.
    :param operation: Тип операции (DEPOSIT или WITHDRAW).
    :param amount: Сумма операции.
    :raises HTTPException: Если кошелек не найден, недостаточно средств или тип операции некорректен.
    """
    logger.info(f"Starting operation {operation} for wallet {wallet_uuid} with amount {amount}")

    if amount <= 0:
        logger.error("Invalid amount")
        print("Amount must be greater than zero")
        return False

    if operation not in {"DEPOSIT", "WITHDRAW"}:
        logger.error("Invalid operation type")
        print("Invalid operation type")
        return False

    async with session.begin():
        result = await session.execute(
            select(Wallet).where(Wallet.UUID == wallet_uuid).with_for_update()
        )
        wallet = result.scalars().first()

        if not wallet:
            logger.error(f"Wallet {wallet_uuid} not found")
            print("Wallet not found")
            return False

        if operation == "WITHDRAW" and wallet.balance < amount:
            logger.error(f"Insufficient funds for wallet {wallet_uuid}")
            print("Insufficient funds")
            return False

        try:
            # Обработка операции
            if operation == "DEPOSIT":
                wallet.balance += amount
            elif operation == "WITHDRAW":
                wallet.balance -= amount

            session.add(wallet)
            await session.commit()
            return True

        except Exception as e:
            logger.error(f"Operation failed: {str(e)}")
            return False


