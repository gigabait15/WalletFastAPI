from typing import Union
from fastapi import FastAPI

app = FastAPI()

wallet = []


@app.get(' api/v1/wallets/{WALLET_UUID}')
async def read_wallet(WALLET_UUID: str):
    """Получение данных кошелька"""
    pass

@app.post(' api/v1/wallets/{WALLET_UUID}/operation')
async def create_operation(WALLET_UUID: str, operation: str, amount: int):
    """Операция пополнения или снятия"""
    if operation == 'DEPOSIT':
        wallet.append(amount)
    elif operation == 'WITHDRAW':
        wallet.remove(amount)

