from config import Config
from models import Wallet, User, Transaction

from modules.general.helpers import get_user_by_id

from hashlib import sha256
from sqlalchemy.orm import Session


def create_hash(transaction_id, user_id, account_id, amount):
    print(f"{account_id}{amount}{transaction_id}{user_id}{Config.SECRET_KEY}")
    return sha256(
        f"{account_id}{amount}{transaction_id}{user_id}{Config.SECRET_KEY}".encode('utf-8')
    ).hexdigest()


def check_signature(transaction_id, user_id, account_id, amount, signature):
    return signature == create_hash(transaction_id, user_id, account_id, amount)


def get_user_wallet(session: Session, user_id, wallet_id) -> Wallet:
    return session.query(
        Wallet
    ).filter(
        Wallet.user_id == user_id,
        Wallet.id == wallet_id
    ).first()


def get_or_create_user_wallet(session: Session, user_id, wallet_id) -> Wallet:
    if get_user_by_id(session, user_id, User):
        if wallet := get_user_wallet(session, user_id, wallet_id):
            return wallet
        wallet = Wallet(
            id=wallet_id,
            user_id=user_id
        )
        session.add(wallet)
        session.commit()
        return wallet
    raise Exception(f"User with id {user_id} not exists")


def get_transaction_by_thirdparty_id(session: Session, thirdparty_id) -> Transaction:
    return session.query(
        Transaction
    ).filter(
        Transaction.thirdparty_id == thirdparty_id
    ).first()


def create_transaction(
        session: Session,
        thirdparty_id,
        user_id,
        account_id,
        amount,
        signature
) -> dict:
    if check_signature(thirdparty_id, user_id, account_id, amount, signature):
        if not get_transaction_by_thirdparty_id(session, thirdparty_id):
            try:
                wallet = get_or_create_user_wallet(session, user_id, account_id)
                transaction = Transaction(
                    thirdparty_id=thirdparty_id,
                    wallet_id=wallet.id,
                    amount=amount
                )
                session.add(transaction)
                session.commit()
                return {"ok": True}
            except Exception as e:
                return {"ok": False, "error": str(e)}
        return {"ok": False, "error": f"Transaction with thirdparty_id {thirdparty_id} already exists"}
    return {"ok": False, "error": "Invalid signature"}
