import psycopg2
from psycopg2 import sql
import os

# Функция для создания базы данных и таблицы
def create_users_database():
    connection = None

    try:
        # Подключение к PostgreSQL
        connection = psycopg2.connect(
            dbname='Users',
            user="postgres",
            password="1234",
            host="localhost",
            options="-c client_encoding=utf-8"
        )

        # Создание курсора
        cursor = connection.cursor()

        # Создание таблицы UsersDate
        create_table_query = """
        CREATE TABLE IF NOT EXISTS UsersDate (
            id SERIAL PRIMARY KEY,
            login VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        );
        """
        cursor.execute(create_table_query)

        # Завершение транзакции
        connection.commit()

        print("База данных и таблица успешно созданы.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

    finally:
        # Закрытие соединения
        if connection:
            connection.close()

# Вызов функции для создания базы данных и таблицы
create_users_database()
