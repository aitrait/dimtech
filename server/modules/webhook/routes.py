from sanic import Blueprint, Request, json

from .helpers import create_transaction
from db import get_db_session

from uuid import UUID

webhook_bp = Blueprint("webhook", url_prefix="/webhook")


@webhook_bp.route("/", methods=["POST"])
async def index(request: Request):
    session = get_db_session()

    kwargs = {
        "thirdparty_id": request.json.get("transaction_id"),
        "amount": request.json.get("amount"),
        "signature": request.json.get("signature"),
        "session": session
    }

    for key in ["user_id", "account_id"]:
        try:
            kwargs[key] = UUID(request.json.get(key))
        except Exception:
            return {"ok": False, "error": f"{key} must be UUID"}

    return json(
        create_transaction(**kwargs)
    )
