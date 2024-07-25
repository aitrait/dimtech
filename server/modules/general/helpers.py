from sqlalchemy import func, String
from sqlalchemy.orm import Session


def get_user_by_email(session: Session, email, Model):
    return session.query(
        Model
    ).filter(
        Model.email == email
    ).first()


def get_user_by_id(session: Session, id, Model):
    return session.query(
        Model
    ).filter(
        Model.id == id
    ).first()


def get_user_info_by_email(session: Session, email, Model) -> dict:
    return session.query(
        func.cast(Model.id, String).label("id"),
        Model.full_name,
        Model.email
    ).filter(
        Model.email == email
    ).first()._asdict()
