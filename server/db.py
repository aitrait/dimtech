from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from config import Config


def get_db_session() -> Session:
    bind = create_engine(Config.DB_CONNECTION_ALEMBIC, echo=True)
    return sessionmaker(
        bind,
        class_=Session,
        expire_on_commit=False
    )()


def get_async_db_session() -> AsyncSession:
    bind = create_async_engine(Config.DB_CONNECTION, echo=True)
    return sessionmaker(
        bind,
        class_=AsyncSession,
        expire_on_commit=False
    )()
