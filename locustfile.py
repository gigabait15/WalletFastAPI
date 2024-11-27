from locust import HttpUser, TaskSet, task, between
import logging

# Настроим логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WalletUserBehavior(TaskSet):
    """
    Класс, описывающий поведение пользователя для тестирования кошельков.
    """

    def on_start(self):
        """
        Выполняется при старте теста. Создаем кошелек для использования в тестах.
        """
        response = self.client.post("/api/v1/wallets/", json={"initial_balance": 1000000})
        if response.status_code == 201:
            self.wallet_uuid = response.json()['UUID']
            logger.info(f"Wallet created with UUID: {self.wallet_uuid}")
        else:
            # Если кошелек не создан, прекращаем выполнение теста
            logger.error(f"Failed to create wallet: {response.status_code} - {response.text}")
            raise Exception("Failed to create wallet during on_start")

    @task
    def deposit(self):
        """
        Тест операции пополнения кошелька.
        """
        response = self.client.post(f"/api/v1/wallets/{self.wallet_uuid}/operation", json={
            "operationType": "DEPOSIT",
            "amount": 1000
        })
        if response.status_code == 200:
            logger.info(f"Deposit successful for wallet {self.wallet_uuid}")
        else:
            logger.error(f"Deposit failed for wallet {self.wallet_uuid}: {response.status_code} - {response.text}")

    @task
    def withdraw(self):
        """
        Тест операции снятия средств с кошелька.
        """
        response = self.client.post(f"/api/v1/wallets/{self.wallet_uuid}/operation", json={
            "operationType": "WITHDRAW",
            "amount": 1000
        })
        if response.status_code == 200:
            logger.info(f"Withdraw successful for wallet {self.wallet_uuid}")
        else:
            logger.error(f"Withdraw failed for wallet {self.wallet_uuid}: {response.status_code} - {response.text}")


class WalletUser(HttpUser):
    """
    Главный класс пользователя для Locust.
    """
    tasks = [WalletUserBehavior]
    wait_time = between(0.0, 0.0001)

    min_wait = 0  
    max_wait = 0