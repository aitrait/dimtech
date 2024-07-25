from db import get_db_session
from models import User, Admin, Wallet

from uuid import UUID


data = {
    Admin: [
        {
            "email": "admin111@admin.com",
            "password": "admin",
            "full_name": "Тестовый Администратор"
        }
    ],
    User: [
        {
            "id": UUID("7772e95f-fc21-40be-9931-5a2740a0da94"),
            "email": "user@user.com",
            "password": "user",
            "full_name": "Тестовый Пользователь"
        }
    ],
    Wallet: [
        {
            "user_id": UUID("7772e95f-fc21-40be-9931-5a2740a0da94")
        }
    ]
}


def load_data():
    session = get_db_session()
    for key, value in data.items():
        print(f"load init {key} data")
        for row in value:
            obj = key(**row)
            session.add(obj)
        session.commit()


if __name__ == "__main__":
    load_data()