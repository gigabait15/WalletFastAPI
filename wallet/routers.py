import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from wallet.models import Wallet
from wallet.wallet_service import get_wallet_balance, perform_wallet_operation
from wallet.schemas import WalletOperation, WalletResponse, WalletCreate

router = APIRouter()


@router.post("/wallets/", response_model=WalletResponse, status_code=201)
async def create_wallet(wallet: WalletCreate, session: AsyncSession = Depends(get_session)):
    """
    Обработчик для создания нового кошелька.

    - **wallet**: Схема WalletCreate с начальными данными кошелька.
    - **session**: Асинхронная сессия базы данных.
    - **return**: Ответ с информацией о созданном кошельке.
    """
    wallet_uuid = str(uuid.uuid4())
    new_wallet = Wallet(UUID=wallet_uuid, balance=wallet.initial_balance)

    async with session.begin():
        session.add(new_wallet)

    return WalletResponse(UUID=wallet_uuid, balance=wallet.initial_balance)


@router.get("/wallets/{wallet_uuid}", response_model=WalletResponse)
async def get_balance(wallet_uuid: str, session: AsyncSession = Depends(get_session)):
    """
    Обработчик для получения баланса кошелька.

    - **wallet_uuid**: UUID кошелька.
    - **session**: Асинхронная сессия базы данных.
    - **return**: Ответ с текущим балансом кошелька.
    """
    balance = await get_wallet_balance(session, wallet_uuid)
    if balance is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return WalletResponse(UUID=wallet_uuid, balance=balance)


@router.post("/wallets/{wallet_uuid}/operation", status_code=200)
async def wallet_operation(
        wallet_uuid: str, operation: WalletOperation, session: AsyncSession = Depends(get_session)
):
    """
    Обработчик для выполнения операций с кошельком.

    - **wallet_uuid**: UUID кошелька.
    - **operation**: Операция (DEPOSIT или WITHDRAW) с суммой.
    - **session**: Асинхронная сессия базы данных.
    - **return**: Статус выполнения операции.
    """
    success = await perform_wallet_operation(session, wallet_uuid, operation.operationType, operation.amount)

    if not success:
        raise HTTPException(status_code=400, detail="Operation failed")

    return {"status": "success"}
