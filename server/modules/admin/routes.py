from sanic import Blueprint, Request, json, html

from modules.general.helpers import get_user_info_by_email
from modules.admin.helpers import (
    get_all_users,
    delete_user_by_email,
    create_user,
    update_user_by_id,
    get_user_wallets_by_email
)
from models import Admin
from auth import auth_admin
from db import get_db_session
from templates import template_env


admin_bp = Blueprint("admin", url_prefix="/admin")


@admin_bp.route("/")
@auth_admin.login_required
async def index(request: Request):
    template = template_env.get_template("admin/index.html")
    email = auth_admin.username(request)
    return html(
        template.render(get_user_info_by_email(get_db_session(), email, Admin))
    )


@admin_bp.route("/get_me")
@auth_admin.login_required
async def get_me(request: Request):
    email = auth_admin.username(request)
    return json(
        get_user_info_by_email(get_db_session(), email, Admin)
    )


@admin_bp.route("/get_users")
@auth_admin.login_required
async def get_users(request: Request):
    return json(
        get_all_users(get_db_session())
    )


@admin_bp.route("/delete_user", methods=['POST'])
@auth_admin.login_required
async def delete_user(request: Request):
    email = request.form.get("user_email", "none")
    return json(
        delete_user_by_email(get_db_session(), email)
    )


@admin_bp.route("/create_user", methods=['POST'])
@auth_admin.login_required
async def create_userr(request: Request):
    return json(
        create_user(get_db_session(), **{key: request.form.get(key) for key in request.form.keys()})
    )


@admin_bp.route("/update_user", methods=['POST'])
@auth_admin.login_required
async def update_user(request: Request):
    return json(
        update_user_by_id(get_db_session(), **{key: request.form.get(key) for key in request.form.keys()})
    )


@admin_bp.route("/user_wallets", methods=['POST'])
@auth_admin.login_required
async def get_user_pays(request: Request):
    email = request.form.get("user_email", "none")
    return json(
        get_user_wallets_by_email(get_db_session(), email)
    )
