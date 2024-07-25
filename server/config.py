import os


class Config:
    SECRET_KEY = os.environ['SECRET_KEY']
    DB_USER = os.environ['POSTGRES_USER']
    DB_PASSWORD = os.environ['POSTGRES_PASSWORD']
    DB_HOST = os.environ['DB_HOST']
    DB_NAME = os.environ['POSTGRES_DB']
    DB_CONNECTION = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    DB_CONNECTION_ALEMBIC = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
