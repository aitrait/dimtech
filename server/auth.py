from db import get_db_session
from models import User, Admin

from sanic_httpauth import HTTPBasicAuth


def authenticate(email, password, model):

    if not email or not password:
        return False

    session = get_db_session()
    user: model = session.query(model).filter(model.email == email).first()

    if not user or user.password != password:
        return False

    return True


auth = HTTPBasicAuth()
auth_admin = HTTPBasicAuth()


@auth.verify_password
def verify_password(email, password):
    return authenticate(email, password, User)


@auth_admin.verify_password
def verify_password_admin(email, password):
    return authenticate(email, password, Admin)
