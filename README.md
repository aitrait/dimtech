# dimtech

Запуск:
1. docker compose up
2. docker exec -it <dimtech_server_container_id> bash
3. (внутри контейнера) alembic upgrade head
4. (внутри контейнера) python3 test_data.py

Управление тестовыми данными осуществляется в файле test_data.py

SECRET_KEY указывается в файле .env

URL:
localhost:8229/admin/ - панель администратора
localhost:8229/user/ - панель пользователя
localhost:8229/webhook/ - вебхук


Запуск без докера:
1. В системе должны быть определены переменные окружения как в файле .env и установлены необходимые зависимости
2. uvicorn --host 0.0.0.0 --port 8080 asgi:app
