from sanic import Sanic
from sanic.response import json

from config import Config
from auth import auth
from modules.user import user_bp
from modules.admin import admin_bp
from modules.webhook import webhook_bp
from db import get_async_db_session

from sqlalchemy import select
from models import User


def create_app() -> Sanic:
    app = Sanic("DimTech_Test", strict_slashes=True)

    app.blueprint(user_bp)
    app.blueprint(webhook_bp)
    app.blueprint(admin_bp)

    app.config.update_config(Config)

    @app.route('/healthcheck')
    @auth.login_required
    async def healthcheck(request):
        async with get_async_db_session() as session:
            query = select(User)
            result = await session.execute(query)
            user = result.scalar()
            print(user)
        return json({"status": "OK"})

    return app
