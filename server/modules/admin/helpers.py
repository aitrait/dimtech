from models import User, Wallet, Transaction
from db import get_db_session
from modules.general.helpers import get_user_by_email, get_user_by_id

from sqlalchemy import func
from sqlalchemy.orm import Session

from uuid import UUID


def get_all_users(session: Session) -> dict:
    return session.query(
        func.json_agg(
            func.json_build_object(
                "id", User.id,
                "email", User.email,
                "full_name", User.full_name
            )
        ).label("users")
    ).select_from(
        User
    ).first()._asdict()


def delete_user_by_email(session: Session, email: str) -> dict:
    session = get_db_session()
    user = get_user_by_email(session, email, User)
    if not user:
        return {"ok": False, "error": f"User with email {email} not found"}
    session.delete(user)
    session.commit()
    return {"ok": True}


def create_user(session: Session, email: str, full_name: str, password: str) -> dict:
    if not get_user_by_email(session, email, User):
        user = User(
            email=email,
            full_name=full_name,
            password=password
        )
        session.add(user)
        session.commit()
        return {"ok": True}
    return {"ok": False, "error": f"User with email {email} already exists"}


def update_user_by_id(session: Session, id, email: str, full_name: str, password: str) -> dict:
    if user := get_user_by_id(session, UUID(id), User):
        user.email = email
        user.password = password
        user.full_name = full_name
        session.commit()
        return {"ok": True}
    return {"ok": False, "error": f"User with id {id} not exists"}


def get_user_wallets_by_email(session: Session, email: str) -> dict:
    if user := get_user_by_email(session, email, User):
        return [i._asdict() for i in session.query(
            func.SUM(Wallet.amount).label("all_amount"),
            func.json_agg(
                func.json_build_object(
                    "id", Wallet.id,
                    "amount", Wallet.amount,
                    "transactions", session.query(
                        func.json_agg(
                            func.json_build_object(
                                "id", Transaction.id,
                                "amount", Transaction.amount,
                                "created", Transaction.created,
                            )
                        )
                    ).filter(Transaction.wallet_id == Wallet.id)
                )
            ).label("wallets")
        ).select_from(
            User
        ).join(
            Wallet, Wallet.user_id == User.id
        ).filter(
            Wallet.user_id == user.id
        ).group_by(User.id).all()]
    return {"ok": False, "error": f"User with email {email} not exists"}
