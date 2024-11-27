from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestWallet:
    wallet_uuid = None

    def test_create_wallet(self):
        response = client.post("/wallets/", json={"initial_balance": 100})
        assert response.status_code == 201
        data = response.json()
        assert "UUID" in data
        assert "balance" in data
        assert data["balance"] == 100
        self.wallet_uuid = data["UUID"]

    def test_get_balance(self):
        assert self.wallet_uuid is not None
        response = client.get(f"/wallets/{self.wallet_uuid}")
        assert response.status_code == 200
        data = response.json()
        assert "UUID" in data
        assert "balance" in data
        assert data["balance"] == 100
        assert data["UUID"] == self.wallet_uuid

    def test_wallet_operation_deposit(self):
        assert self.wallet_uuid is not None
        response = client.post(
            f"/wallets/{self.wallet_uuid}/operation",
            json={"operationType": "DEPOSIT", "amount": 50},
        )
        assert response.status_code == 200
        data = response.json()
        assert data == {"status": "success"}

        response = client.get(f"/wallets/{self.wallet_uuid}")
        assert response.status_code == 200
        data = response.json()
        assert data["balance"] == 150

    def test_wallet_operation_withdraw(self):
        assert self.wallet_uuid is not None
        response = client.post(
            f"/wallets/{self.wallet_uuid}/operation",
            json={"operationType": "WITHDRAW", "amount": 30},
        )
        assert response.status_code == 200
        data = response.json()
        assert data == {"status": "success"}

        response = client.get(f"/wallets/{self.wallet_uuid}")
        assert response.status_code == 200
        data = response.json()
        assert data["balance"] == 120


# оставил второй вариант теста
import pytest

@pytest.fixture
def create_wallet():
    response = client.post('/api/v1/wallets/', json={'initial_balance': 0})
    assert response.status_code == 201
    wallet_uuid = response.json()['UUID']
    return wallet_uuid

@pytest.mark.asyncio
async def test_get_wallet(create_wallet):
    wallet_uuid = create_wallet
    assert wallet_uuid is not None

    response = client.get(f'/api/v1/wallets/{wallet_uuid}')
    print(response.json())
    assert response.status_code == 200
    assert response.json()['UUID'] == wallet_uuid