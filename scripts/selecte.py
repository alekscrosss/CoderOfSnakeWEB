import psycopg2
from psycopg2 import extras
import os
from dotenv import load_dotenv
load_dotenv()

# Параметри підключення до бази даних PostgreSQL
dbname = os.environ.get('POSTGRES_DB')
user = os.environ.get('POSTGRES_USER')
password = os.environ.get('POSTGRES_PASSWORD')
host = "localhost"  # або адреса вашого сервера PostgreSQL
port = os.environ.get('POSTGRES_PORT')  # порт за замовчуванням для PostgreSQL

# Встановлення з'єднання з базою даних
conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

# Створення курсора для виконання SQL-запитів
cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

# Виконання SQL-запиту для перегляду вмісту таблиці
cursor.execute('SELECT * FROM users')
cursor.execute('SELECT * FROM photos')
# cursor.execute('SELECT * FROM users WHERE FALSE')
# cursor.execute('SELECT * FROM photos WHERE FALSE')

# Отримання опису стовпців
columns = [desc[0] for desc in cursor.description]

# Виведення заголовків стовпців
print(columns)
rows = cursor.fetchall()
for row in rows:
    print(row)
# Закриття курсора та з'єднання
cursor.close()
conn.close()
