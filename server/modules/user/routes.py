from sanic import Blueprint, Request, json, html

from modules.general.helpers import get_user_info_by_email
from modules.user.helpers import get_wallets_by_email, get_transactions_by_email
from models import User
from auth import auth
from db import get_db_session
from templates import template_env


user_bp = Blueprint("user", url_prefix="/user")


@user_bp.route("/")
@auth.login_required
async def index(request: Request):
    template = template_env.get_template("user/index.html")
    email = auth.username(request)
    return html(
        template.render(get_user_info_by_email(get_db_session(), email, User))
    )


@user_bp.route("/get_me")
@auth.login_required
async def get_me(request: Request):
    email = auth.username(request)
    return json(
        get_user_info_by_email(get_db_session(), email, User)
    )


@user_bp.route("/get_wallets")
@auth.login_required
async def get_wallets(request: Request):
    email = auth.username(request)
    return json(
        get_wallets_by_email(get_db_session(), email)
    )


@user_bp.route("/get_transactions")
@auth.login_required
async def get_transactions(request: Request):
    email = auth.username(request)
    return json(
        get_transactions_by_email(get_db_session(), email)
    )
