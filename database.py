from sqlalchemy.ext.asyncio import create_async_engine, AsyncAttrs, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase, declared_attr
from config import settings


DATABASE_URL = settings.get_db_url()

engine = create_async_engine(DATABASE_URL, echo=True)

async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class Base(AsyncAttrs, DeclarativeBase):
    """Абстрактный класс для создания таблиц"""
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}"
