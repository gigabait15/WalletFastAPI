import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import text, create_engine


load_dotenv()


class Settings(BaseSettings):
    """Класс модели для доступа к переменным окружения"""
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    SECRET_KEY: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )

    def create_database(self):
        """Функция создания базы данных"""
        if self.DB_PASSWORD is not None:
            full_url = f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}"
        else:
            full_url = f"postgresql://{self.DB_USER}@{self.DB_HOST}:{self.DB_PORT}"

        temp_engine = create_engine(full_url , isolation_level='AUTOCOMMIT')

        with temp_engine.connect() as conn:
            try:
                result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{self.DB_NAME}'"))
                db_exists = result.scalar()

                if not db_exists:
                    conn.execute(text(f"CREATE DATABASE {settings.DB_NAME};"))
                    return True
                else:
                    return None

            except Exception as e:
                print(f'Ошибка при создании БД: {e}')
            finally:
                conn.close()

    def get_url(self):
        """
        Функция для формирования ссылки на БД
        :return:ссылку на БД
        """
        if self.DB_PASSWORD is not None:
            return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return f"postgresql+asyncpg://{self.DB_USER}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


# объявление переменной для обращение к экземпляру класса
settings = Settings()
