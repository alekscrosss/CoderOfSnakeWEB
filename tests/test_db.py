import psycopg2
from psycopg2 import OperationalError
import os
from dotenv import load_dotenv
load_dotenv()
def create_connection():
    try:
        conn = psycopg2.connect(
            database=os.environ.get('POSTGRES_DB'),
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD'),
            host="localhost",
            port=os.environ.get('POSTGRES_PORT'),
        )
        print("Соединение с базой данных успешно установлено")
        conn.close()
    except OperationalError as e:
        print(f"Ошибка при подключении к базе данных: {e}")

create_connection()
