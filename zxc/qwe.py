import psycopg2
from passlib.hash import pbkdf2_sha256
from psycopg2 import sql
import os
from flask import Flask, render_template, request, redirect, url_for

class AuthService:
    def __init__(self):
        project_folder = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(project_folder, 'mydatabase.db')
        self.connection = psycopg2.connect(
            dbname=db_path,
            user="postgres",
            password="1234",
            host="localhost"
        )
        
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS UserData (
            id SERIAL PRIMARY KEY,
            login VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        );
        """
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def register(self, login, password):
        hashed_password = self._hash_password(password)
        try:
            insert_query = sql.SQL("INSERT INTO UserData (login, password) VALUES ({}, {});").format(
                sql.Literal(login),
                sql.Literal(hashed_password)
            )
            self.cursor.execute(insert_query)
            self.connection.commit()
            print("Регистрация прошла успешно!")
        except psycopg2.IntegrityError:
            print("Пользователь с таким логином уже существует.")
        except Exception as e:
            print(f"Произошла ошибка при регистрации: {e}")

    def login(self, login, password):
        try:
            select_query = sql.SQL("SELECT password FROM UserData WHERE login = {};").format(
                sql.Literal(login)
            )
            self.cursor.execute(select_query)
            result = self.cursor.fetchone()

            if result and self._check_password(password, result[0]):
                print("Вход выполнен успешно!")
                return True
            else:
                print("Неверный логин или пароль.")
        except Exception as e:
            print(f"Произошла ошибка при входе: {e}")
        return False

    def _hash_password(self, password):
        return pbkdf2_sha256.hash(password)

    def _check_password(self, plain_password, hashed_password):
        return pbkdf2_sha256.verify(plain_password, hashed_password)

    def close_connection(self):
        self.connection.close()

app = Flask(__name__)
auth_service = AuthService()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    login = request.form['login']
    password = request.form['password']

    auth_service.register(login, password)

    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    login = request.form['login']
    password = request.form['password']

    if auth_service.login(login, password):
        return "Вход выполнен успешно!"
    else:
        return "Неверный логин или пароль."

if __name__ == '__main__':
    app.run(debug=True)
