from models import User, Wallet, Transaction

from sqlalchemy import func
from sqlalchemy.orm import Session


def get_wallets_by_email(session: Session, email) -> dict:
    return session.query(
        func.SUM(Wallet.amount).label("all_amount"),
        func.json_agg(
            func.json_build_object(
                "wallet_id", Wallet.id,
                "amount", Wallet.amount
            )
        ).label("wallets")
    ).select_from(
        User
    ).join(
        Wallet, Wallet.user_id == User.id
    ).filter(
        User.email == email
    ).first()._asdict()


def get_transactions_by_email(session: Session, email) -> dict:
    return session.query(
        func.json_agg(
            func.json_build_object(
                "wallet_id", Wallet.id,
                "amount", Transaction.amount,
                "created", Transaction.created,
            )
        ).label("transactions")
    ).select_from(
        Transaction
    ).join(
        Wallet, Wallet.id == Transaction.wallet_id
    ).join(
        User, User.id == Wallet.user_id
    ).filter(
        User.email == email
    ).group_by(User.id).first()
