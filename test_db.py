import psycopg2
from psycopg2 import OperationalError

def create_connection():
    try:
        conn = psycopg2.connect(
            database="db2",
            user="postgres",
            password="567234",
            host="localhost",
            port="5432",
        )
        print("Соединение с базой данных успешно установлено")
        conn.close()
    except OperationalError as e:
        print(f"Ошибка при подключении к базе данных: {e}")

create_connection()