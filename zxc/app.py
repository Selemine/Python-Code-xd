from validate_email import validate_email
from flask import Flask, render_template, request, redirect, url_for
from passlib.hash import pbkdf2_sha256
from flask_mail import Mail
import sqlite3 
import os
from flask.globals import g
import secrets
from flask_mail import Message
from flask import render_template

class AuthService:
    def __init__(self, app):
        self.app = app

    def get_db(self):
        if 'db_connection' not in g:
            g.db_connection = sqlite3.connect(self.app.config['DATABASE'])
            g.db_connection.row_factory = sqlite3.Row
        return g.db_connection

    def create_table(self):
        with self.app.app_context():
            connection = self.get_db()
            cursor = connection.cursor()
            create_table_query = """
            CREATE TABLE IF NOT EXISTS UsersDate (
                id INTEGER PRIMARY KEY,
                login TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
            """
            cursor.execute(create_table_query)
            connection.commit()

    def register(self, email, password):
        if not validate_email(email):
            print("Некорректный формат электронной почты.")
            return

        self.create_table()
        hashed_password = self._hash_password(password)
        try:
            with self.app.app_context():
                connection = self.get_db()
                cursor = connection.cursor()
                # Заменил "email" на "login" в запросе SQL
                insert_query = "INSERT INTO UsersDate (login, password) VALUES (?, ?);"
                cursor.execute(insert_query, (email, hashed_password))
                connection.commit()
                print("Регистрация прошла успешно!")
        except sqlite3.IntegrityError:
            print("Пользователь с таким email уже существует.")
        except Exception as e:
            print(f"Произошла ошибка при регистрации: {e}")

    def login(self, login, password):
        try:
            with self.app.app_context():
                connection = self.get_db()
                cursor = connection.cursor()
                select_query = "SELECT password FROM UsersDate WHERE login = ?;"
                cursor.execute(select_query, (login,))
                result = cursor.fetchone()

                if result and self._check_password(password, result[0]):
                    print("Вход выполнен успешно!")
                    return True
                else:
                    print("Неверный логин или пароль.")
        except Exception as e:
            print(f"Произошла ошибка при входе: {e}")
        return False
    
    def generate_reset_token(self, login):
        reset_token = secrets.token_urlsafe(32)  # Генерация случайного токена
        with self.app.app_context():
            connection = self.get_db()
            cursor = connection.cursor()
            update_query = "UPDATE UsersDate SET reset_token = ? WHERE login = ?;"
            cursor.execute(update_query, (reset_token, login))
            connection.commit()
        return reset_token

    def _hash_password(self, password):
        return pbkdf2_sha256.hash(password)

    def _check_password(self, plain_password, hashed_password):
        return pbkdf2_sha256.verify(plain_password, hashed_password)
    
    def send_reset_email(self, login, reset_token):
        reset_link = url_for('reset_password', reset_token=reset_token, _external=True)
        subject = "Сброс пароля"
        body = f"Для сброса пароля перейдите по следующей ссылке: {reset_link}"
        recipients = [self.get_user_email(login)]  
        
        if recipients[0]:
            message = Message(subject=subject, body=body, recipients=recipients)
            mail.send(message)
            print("Инструкции по сбросу пароля отправлены на вашу почту.")
        else:
            print("Пользователь с таким логином не найден.")

    def get_user_email(self, login):
        with self.app.app_context():
            connection = self.get_db()
            cursor = connection.cursor()
            select_query = "SELECT email FROM UsersDate WHERE login = ?;"
            cursor.execute(select_query, (login,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        # ФУНКЦИИ ДЛЯ ВОССТАНОВЛЕНИЯ ПАРОЛЯ  
    def forgot_password():
        if request.method == 'POST':
            login = request.form['login']
           
            reset_token = auth_service.generate_reset_token(login)
            auth_service.send_reset_email(login, reset_token)
            return redirect(url_for('index'))
        return render_template('forgot_password.html')

    def send_reset_email(login, reset_token):
        reset_link = url_for('reset_password', reset_token=reset_token, _external=True)
        subject = "Сброс пароля"
        body = f"Для сброса пароля перейдите по следующей ссылке: {reset_link}"
        recipients = [get_user_email(login)]  
        message = Message(subject=subject, body=body, recipients=recipients)
        mail.send(message)


app = Flask(__name__)
app.config['DATABASE'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.db')

auth_service = AuthService(app)
app.config['MAIL_SERVER'] = 'your_mail_server'
app.config['MAIL_PORT'] = 587  # порт вашего SMTP-сервера
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'your_username'
app.config['MAIL_PASSWORD'] = 'your_password'

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    login = request.form['login']
    password = request.form['password']

    auth_service.register(login, password)

    return redirect(url_for('index'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        login = request.form['login']
        reset_token = auth_service.generate_reset_token(login)
        auth_service.send_reset_email(login, reset_token)
        return redirect(url_for('index'))
    return render_template('forgot_password.html')

@app.route('/reset_password', methods=['POST'])
def reset_password():
    return "Ссылка для сброса пароля отправлена на ваш email!"  # Или перенаправление на другую страницу


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
