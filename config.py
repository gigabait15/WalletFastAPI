import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine, text


load_dotenv()


DATABASE_URL = f"postgresql+asyncpg"

class Settings(BaseSettings):
    """Класс модели для доступа к переменным окружения"""
    DB_HOST : str
    DB_PORT : int
    DB_NAME : str
    DB_USER : str
    DB_PASSWORD : str
    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(
        env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".." ,".env")
    )

    def create_database(self):
        """Функция создания БД"""
        if self.DB_PASSWORD is not None:
            temp_engine = create_engine(f"{DATABASE_URL}://{self.DB_USER}:{self.DB_PASSWORD}"
                                        f"@{self.DB_HOST}:{self.DB_PORT}", isolation_level='AUTOCOMMIT')
        else:
            temp_engine = create_engine(f"{DATABASE_URL}://{self.DB_USER}"
                                        f"@{self.DB_HOST}:{self.DB_PORT}", isolation_level='AUTOCOMMIT')

        with temp_engine.connect() as conn:
            try:
                conn.execute(text(f"CREATE DATABASE {self.DB_NAME};"))
                print(f'База данных {self.DB_NAME} успешно создана')
            except Exception as e:
                print(f'Ошибка при создании БД: {e}')
            finally:
                conn.close()

    def get_db_url(self) -> str:
        """Функция возвращает ссылку на подключение к БД"""
        if self.DB_PASSWORD is not None:
            return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}"
                    f":{self.DB_PORT}/{settings.DB_NAME}")
        return f"postgresql+asyncpg://{self.DB_USER}@{self.DB_HOST}:{self.DB_PORT}/{settings.DB_NAME}"

    def get_auth_data(self) -> dict[str, str]:
        """Функция возвращает словарь с данными ключа приложения и алгоритма шифрования"""
        return {'secret_key': self.SECRET_KEY, 'algorithm': self.ALGORITHM}



# объявление переменной для ображение к экземпляру класса
settings = Settings()

