from sqlalchemy import ForeignKey, Column, UUID, Float, DateTime, String, func, event
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils.types import EmailType, PasswordType

from db import get_db_session

import uuid

# ABSTRACT

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class EmailPassword(BaseModel):
    __abstract__ = True
    email = Column(EmailType, unique=True)
    full_name = Column(String(256), nullable=False)
    password = Column(PasswordType(
        schemes=['pbkdf2_sha512']
    ))


# MODELS


class Admin(EmailPassword):
    __tablename__ = "admin"


class User(EmailPassword):
    __tablename__ = "user"


class Wallet(BaseModel):
    __tablename__ = "wallet"

    amount = Column(Float, default=0)
    user_id = Column(UUID, ForeignKey("user.id", ondelete='CASCADE'))
    user = relationship("User", cascade="all,delete", )


class Transaction(BaseModel):
    __tablename__ = "transaction"

    thirdparty_id = Column(String(256), unique=True)
    amount = Column(Float)
    wallet_id = Column(UUID, ForeignKey("wallet.id", ondelete='CASCADE'))
    wallet = relationship("Wallet", cascade="all,delete")
    created = Column(DateTime, default=func.current_timestamp())


@event.listens_for(Transaction, "after_insert")
def after_create_transaction(mapper, connection, target):
    session = get_db_session()
    if wallet := session.query(
        Wallet
    ).filter(
        Wallet.id == target.wallet_id
    ).first():
        wallet.amount += target.amount
        session.add(wallet)
        session.commit()


@event.listens_for(Transaction, "after_delete")
def after_delete_transaction(mapper, connection, target):
    session = get_db_session()
    if wallet := session.query(
        Wallet
    ).filter(
        Wallet.id == target.wallet_id
    ).first():
        wallet.amount -= target.amount
        session.add(wallet)
        session.commit()
