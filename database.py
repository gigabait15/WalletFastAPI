from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, declared_attr
from config import settings


engine = create_async_engine(
    settings.get_url(),
    echo=True
)
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_session() -> AsyncSession:
    """
    Получает сессию для работы с базой данных.
    :return: Асинхронная сессия SQLAlchemy.
    """
    async with async_session_maker() as session:
        yield session



class Base(AsyncAttrs, DeclarativeBase):
    """Абстрактный класс для создания таблиц"""
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"
